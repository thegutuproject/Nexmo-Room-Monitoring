# import the necessary packages
import nexmo
from imgurpython import ImgurClient
import os
import cv2
import urllib
import argparse
import datetime
import imutils
import time
import requests
import pprint
from flask import Flask
from flask import request
import urllib
import urllib2


def getPinURL(imgurClientId, imgurClientSecret):
    """build a URL for the user to navigate to and "Allow" the application"""

    response = "pin"
    # can be any string at all
    state = "anything"
    url = r"https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}"

    print "browse to the following URL and grab the pin:"
    pin_url = url.format(cid = imgurClientId, resp = response, app_state = state)
    print pin_url

    return pin_url


def exchangePinForTokens(imgurClientId, imgurClientSecret, pin):
    """takes the client_id and client_secret from the registered application URL,
   along with the pin returned from `getPin()`, and return an access_token and a
   refresh_token"""

    # the query parameters you'll send along with the POST request
    params = {"client_id": imgurClientId,
              "client_secret": imgurClientSecret,
              "grant_type": "pin",
              "pin": pin}

    url = r"https://api.imgur.com/oauth2/token/"

    # make sure the data is sent with the POST request, along with disabling the
    # SSL verification, potential security warning
    r = requests.post(url, data=params, verify=False)
    j = r.json()
    print "The exchangePinForTokens API response:"
    pprint.pprint(j)

    # add the access_token to the headers as
    # Authorization: Bearer YOUR_ACCESS_TOKEN
    access_token = j['access_token']
    refresh_token = j['refresh_token']
    print "Access Token: {0}\nRefresh Token: {1}".format(access_token, refresh_token)
    return (access_token, refresh_token)


def uploadImage(access_token, image_url):
    """uploads an image using it's URL, the access_token is required"""

    # need to include the authorization headers,
    # in order to make use of the access token
    headers = {"authorization": "Bearer {0}".format(access_token)}

    upload_url = r'https://api.imgur.com/3/upload'

    # this is the data we'll POST to the api's URL
    payload = {'image': image_url,
               'type': 'url',
               'title': "WORKS"}

    # make the upload, ensuring that the data, headers are included, and
    # make sure to disable the verification of the SSL. Potential insecurty though
    r = requests.post(upload_url, data=payload, headers=headers, verify=False)

    # save the json response, print it to screen
    j = r.json()
    print "The UploadImage API response:"
    pprint.pprint(j)

    # print the img URL to verify that the image is still  there
    uploaded_url = j['data']['link']
    print "The uploaded image URL is: {0}".format(uploaded_url)

def messageUser(nexmoClientId, nexmoClientSecret, pinURL):
    params = {
        'api_key': format(nexmoClientId),
        'api_secret': format(nexmoClientSecret),
        'to': '13476772691',
        'from': '13476772691',
        'text': format(pinURL)
    }

    url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)
    print url

    imgurRequest = urllib2.Request(url)
    imgurRequest.add_header('Accept', 'application/json')
    response = urllib2.urlopen(imgurRequest)
    print response


# a popular Python idiom to make sure that the following code gets run when this
# file is ran as __main__, rather than imported
if __name__ == '__main__':
    """Run the following if module is top module"""

    # found here: https://api.imgur.com/oauth2/addclient
    imgurClientId = "abb3bc18c3e725b"
    imgurClientSecret = "d2df58730cc8ed27ed6eb72ebca03aed259707ae"

    nexmoClientId = "5854cac7"
    nexmoClientSecret = "38b0494379178606"

    app = Flask(__name__)

    @app.route('/')
    def index():
        print getPinURL(imgurClientId, imgurClientSecret)
        return getPinURL(imgurClientId, imgurClientSecret)

    @app.route('/message')
    def message():
        print request.get_json()
        return 'yay'


    print "hello"
    # URL needed to have the user visit and allow the application to use the pin
    # THIS URL WILL BE SENT TO USER
    messageUser(getPinURL(imgurClientId, imgurClientSecret))

    # USER WILL THEN LOG IN, TEXT THE PIN BACK

    # ONCE PIN IS RECEIVED, PROCEED

    access_token, refresh_token = exchangePinForTokens(imgurClientId, imgurClientSecret, pin)
    # uploadImage(access_token, image_url)
    app.run(host= '0.0.0.0', port = 65534)

# webCam = cv2.VideoCapture(0)
#
# firstFrame = None
# time.sleep(0.25)
#
# while True:
#     (grabbed, frame) = webCam.read()
#     roomStatus = "Unoccupied"
#
#     if not grabbed:
#         break
#
#     frame = imutils.resize(frame, width=1024)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (21, 21), 0)
#
#     if firstFrame is None:
#         firstFrame = gray
#         continue
#
#     frameDelta = cv2.absdiff(firstFrame, gray)
#     thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
#
#     thresh = cv2.dilate(thresh, None, iterations=3)
#     (hierarchy, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     for c in cnts:
#         # if the contour is too small, ignore it
#         if cv2.contourArea(c) < 4000:
#             continue
#
#         # compute the bounding box for the contour, draw it on the frame,
#         # and update the text
#         (x, y, w, h) = cv2.boundingRect(c)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         roomStatus = "Occupied"
#
#     cv2.putText(frame, "Room Status: {}".format(roomStatus), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#     cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#
#     cv2.imshow("Security Feed", frame)
#     # cv2.imshow("Threshold", thresh)
#     # cv2.imshow("Frame Delta", frameDelta)
#     key = cv2.waitKey(1) & 0xFF
#
#     if key == ord("q"):
#         break
#
#     firstFrame = None
#
# webCam.release()
# cv2.destroyAllWindows()
