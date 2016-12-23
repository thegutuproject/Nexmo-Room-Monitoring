import requests
import pprint
from flask import Flask
from flask import request
import urllib
import urllib2
import json
from datetime import datetime, timedelta, date
import base64


# Get user authentication PIN
def getPinURL(apiKeysAndTokens):
    response = "pin"
    # can be any string at all
    state = "anything"
    url = r"https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}"

    pin_url = url.format(cid=apiKeysAndTokens["imgurClientId"], resp=response, app_state=state)
    print "PIN URL: " + pin_url
    return pin_url


def exchangePinForTokens(apiKeysAndTokens, userAuthorizationPin):
    """takes the client_id and client_secret from the registered application URL,
   along with the pin returned from `getPin()`, and return an access_token and a
   refresh_token"""

    # the query parameters you'll send along with the POST request
    params = {"client_id": apiKeysAndTokens["imgurClientId"],
              "client_secret": apiKeysAndTokens["imgurClientSecret"],
              "grant_type": "pin",
              "pin": format(userAuthorizationPin)}

    url = r"https://api.imgur.com/oauth2/token/"

    # make sure the data is sent with the POST request, along with disabling the
    # SSL verification, potential security warning
    r = requests.post(url, data=params, verify=False)
    j = r.json()
    print "The exchangePinForTokens API response:"
    pprint.pprint(j)

    # add the access_token to the headers as
    # Authorization: Bearer YOUR_ACCESS_TOKEN
    apiKeysAndTokens["imgurAccessToken"] = (j['access_token']).encode('utf-8')
    apiKeysAndTokens["imgurRefreshToken"] = (j['refresh_token']).encode('utf-8')
    apiKeysAndTokens["imgurTokenDate"] = str(datetime.now().date())
    print "Access Token: {0}\nRefresh Token: {1}".format(apiKeysAndTokens["imgurAccessToken"],
                                                             apiKeysAndTokens["imgurRefreshToken"])
    if "imgurAccessToken" in apiKeysAndTokens.keys():
        return True


def uploadImage(apiKeysAndTokens, imgLocation):
    """uploads an image using it's URL, the access_token is required"""

    # need to include the authorization headers,
    # in order to make use of the access token
    headers = {"authorization": "Bearer {0}".format(apiKeysAndTokens["imgurAccessToken"])}

    upload_url = r'https://api.imgur.com/3/upload'

    # this is the data we'll POST to the api's URL
    payload = {'image': encodeImage(imgLocation),
               'type': 'url',
               'title': "INTRUDER DETECTED " + str(datetime.now())}

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


def messageUser(apiKeysAndTokens, pinURL):
    params = {
        'api_key': apiKeysAndTokens["nexmoClientId"],
        'api_secret': apiKeysAndTokens["nexmoClientSecret"],
        'to': '13476772691',
        'from': '12082770230',
        'text': format(pinURL)
    }

    url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)
    print url

    request = urllib2.Request(url)
    request.add_header('Accept', 'application/json')
    response = urllib2.urlopen(request)

    if response.code == 200:
        data = response.read()

        # Decode JSON response from UTF-8
        decoded_response = json.loads(data.decode('utf-8'))
        # Check if your messages are succesful

        messages = decoded_response["messages"]
        for message in messages:
            if message["status"] == "0":
                print "success"
        print response

    else:
        # Check the errors
        print "unexpected http " + response.code + " response from nexmo api"


def encodeImage(imgLocation):
    imgFile = open(imgLocation, 'rb')
    imgBinaryData = imgFile.read()
    imgBinary64Data = base64.b64encode(imgBinaryData)
    return imgBinary64Data


def initialize(apiKeysAndTokens):
    with open("resources.txt") as resourceFile:
        for line in resourceFile:
            (key, val) = line.split()
            apiKeysAndTokens[key] = val
    resourceFile.close()

def writeToFile(apiKeysAndTokens):
    with open("resources.txt", 'w') as resourceFile:
        for (key, value) in apiKeysAndTokens.items():
            resourceFile.write(key + " " + value + "\n")


if __name__ == '__main__':

    apiKeysAndTokens = {}
    initialize(apiKeysAndTokens)

    print apiKeysAndTokens

    app = Flask(__name__)

    @app.route('/')
    def default():
        return "Hello World!"

    @app.route('/initialize')
    def index():
        if "imgurAccessToken" not in apiKeysAndTokens:
            pinURL = getPinURL(apiKeysAndTokens)
            messageUser(apiKeysAndTokens, pinURL)
            return "Initialie - PIN URL: " + pinURL, 200

    @app.route('/userPin')
    def userPin():
        if request is not None:
            userAuthorizationPin = request.args.get('text')

        # If no token date is found, then there is no token
        if 'imgurTokenDate' not in apiKeysAndTokens or apiKeysAndTokens["imgurTokenDate"] is None:
            if exchangePinForTokens(apiKeysAndTokens, userAuthorizationPin):
                writeToFile(apiKeysAndTokens)
                return "", 200

        # If token has expired
        elif (datetime.now().date() - datetime.strptime(apiKeysAndTokens['imgurTokenDate'], "%Y-%m-%d").date()) > timedelta(days=25):
            if exchangePinForTokens(apiKeysAndTokens, userAuthorizationPin):
                writeToFile(apiKeysAndTokens)
                return "", 200

        elif apiKeysAndTokens['imgurAccessToken'] is not None and ((datetime.now().date() - datetime.strptime(apiKeysAndTokens['imgurTokenDate'], "%Y-%m-%d").date()) < timedelta(days=25)):
            print "Already authenticated"
            print apiKeysAndTokens
            return "", 200

    @app.route('/upload')
    def upload():
        uploadImage(apiKeysAndTokens, "intruder.jpg")
        print "Server has been notified of an intruder"

    @app.route('/notify')
    def notify():
        return None
    #
    # URL needed to have the user visit and allow the application to use the pin
    # THIS URL WILL BE SENT TO USER
    #
    # USER WILL THEN LOG IN, TEXT THE PIN BACK
    #
    # ONCE PIN IS RECEIVED, PROCEED

    # access_token, refresh_token = exchangePinForTokens(imgurClientId, imgurClientSecret, pin)
    # uploadImage(access_token, image_url)
    app.run(host='0.0.0.0', port=65534)