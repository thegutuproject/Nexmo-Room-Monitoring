# import the necessary packages

import cv2
import datetime
import imutils
import time
import requests
import urllib2

def initializeRequestServer():
    url = r"0.0.0.0:65534/initialize"

    # r = requests.get(url, data=params, verify=False)
    request = urllib2.Request(url)


def notifyServer():
    params = {"intruderDetected": True}

    url = r"0.0.0.0:65534/upload"

    # r = rqqqequests.get(url, data=params, verify=False)
    request = urllib2.Request(url)


def processVideo(webCam):
    firstFrame = None
    time.sleep(0.25)

    intruderDetected = False
    initializeRequestServer()

    while True:
        (grabbed, frame) = webCam.read()
        roomStatus = "Unoccupied"

        if not grabbed:
            break

        frame = imutils.resize(frame, width=1024)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=3)
        (hierarchy, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 4000:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roomStatus = "Occupied"
            cv2.imwrite('intruder.jpg', frame)
            intruderDetected = True

        cv2.putText(frame, "Room Status: {}".format(roomStatus), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                    2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        cv2.imshow("Security Feed", frame)
        # cv2.imshow("Threshold", thresh)
        # cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        firstFrame = None

        if intruderDetected:
            notifyServer()

    webCam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    webCam = cv2.VideoCapture(0)

    processVideo(webCam)
