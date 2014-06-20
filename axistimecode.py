import cv2
import urllib 
import numpy as np
import datetime as dt


NOTFOUND = -1

URL = None

stream = urllib.urlopen(URL)
bytes=''

while True:

    #Read in bytes from the url stream
    bytes += stream.read(1024)

    #Find the start and end of file markers for each jpg
    startofjpg = bytes.find('\xff\xd8')
    endofjpg = bytes.find('\xff\xd9')

    if startofjpg != NOTFOUND and endofjpg != NOTFOUND:
        jpg = bytes[startofjpg:(endofjpg + 2)] #add 2 to account for the two-bit eof marker
        bytes = bytes[(endofjpg + 2):] #remove the found jpg from the bytes

        startoftimecode = jpg.find('\xff\xfe\x00\x0f\x0a\x01') #find the start of the timecode marker

        #Pull out each of the hex nibbles from the string and parse into an actual hex value
        #Gets five bytes: four bytes are unix time, last byte is hundredths of seconds
        timecode = "".join(hex(ord(n)).replace(r'0x', '').zfill(2) for n in jpg[(startoftimecode + 6):(startoftimecode+ 11)])
        unixtimeinseconds, hundredthsofasecond = timecode[:8], timecode[8:]
        #print unixtimeinseconds, hundredthsofasecond
        datetimeobject = dt.datetime.fromtimestamp(int(unixtimeinseconds, 16))
        datetimeobject = datetimeobject + dt.timedelta(microseconds=(int(hundredthsofasecond, 16) * 10000))
        print datetimeobject.strftime('%Y-%m-%d %H:%M:%S:%f')

        #convert hex string to jpg
        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)

        #display jpg on screen
        cv2.imshow('i',image)
        if cv2.waitKey(1) == 27:
            exit(0)   
