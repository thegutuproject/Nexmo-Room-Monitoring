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
    pin_url = url.format(cid=imgurClientId, resp=response, app_state=state)
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


    @app.route('/initialize')
    def index():
        print getPinURL(imgurClientId, imgurClientSecret)
        return messageUser(getPinURL(imgurClientId, imgurClientSecret))

    @app.route('/userPin')
    def userPin():
        print request.get_json()
        return 'yay'

    @app.route('/upload')
    def upload():

    @app.route('/notify')
    def notify():



    print "hello"
    # URL needed to have the user visit and allow the application to use the pin
    # THIS URL WILL BE SENT TO USER

    # USER WILL THEN LOG IN, TEXT THE PIN BACK

    # ONCE PIN IS RECEIVED, PROCEED

    access_token, refresh_token = exchangePinForTokens(imgurClientId, imgurClientSecret, pin)
    # uploadImage(access_token, image_url)
    app.run(host='0.0.0.0', port=65534)