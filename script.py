import nexmo
from imgurpython import ImgurClient
import os
import cv2
import urllib


imgSources = "./resources/"
catCascade = "haarcascade_frontalcatface.xml"

imgurClientId = "abb3bc18c3e725b"
imgurClientSecret = "d2df58730cc8ed27ed6eb72ebca03aed259707ae"

client = ImgurClient(imgurClientId, imgurClientSecret)

# for filename in os.listdir(imgSources):
#     image = cv2.imread(imgSources + filename)
#     grayScaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # load the cat detector Haar cascade, then detect cat faces
#     # in the input image
#     detector = cv2.CascadeClassifier("./" + catCascade)
#     rectangleBoundaries = detector.detectMultiScale(grayScaleImage, scaleFactor=1.3, minNeighbors=10, minSize=(75, 75))
#
#     # loop over the cat faces and draw a rectangle surrounding each
#     for (i, (x, y, w, h)) in enumerate(rectangleBoundaries):
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         cv2.putText(image, "Cat #{}".format(i + 1), (x, y - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
#
#     # resive image to fit on screen
#     # resizedImage = cv2.resize(image, (1920, 1080))
#
#     # show the detected cat faces
#     # cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
#     cv2.imshow("Cat Faces", image)
#     cv2.waitKey(0)

authorization_url = client.get_auth_url('pin')
print authorization_url

response = urllib.urlopen(authorization_url)
headers = response.info()
data = response.read()

print response
print headers
print data

# credentials = client.authorize('5fbb0b3470', 'pin')
# print credentials
# client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
#
# print (client.upload_from_path("./resources/cat_01.jpg", anon="false"))
