import nexmo
import imgurpython
import os
import cv2


imgSources = "/resources/"

imgurClientId = "abb3bc18c3e725b"
imgurClientSecret = "d2df58730cc8ed27ed6eb72ebca03aed259707ae"

client = imgurpython.ImgurClient(imgurClientId, imgurClientSecret)

for filename in os.listdir(imgSources):
    image = cv2.imread(filename)
    grayScaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # load the cat detector Haar cascade, then detect cat faces
    # in the input image
    detector = cv2.CascadeClassifier(args["cascade"])
    rectangleBoundaries = detector.detectMultiScale(grayScaleImage, scaleFactor=1.04, minNeighbors=20,
                                                    minSize=(600, 600))

    # loop over the cat faces and draw a rectangle surrounding each
    for (i, (x, y, w, h)) in enumerate(rectangleBoundaries):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, "Cat #{}".format(i + 1), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

    # resive image to fit on screen
    resizedImage = cv2.resize(image, (1280, 1024))

    # show the detected cat faces
    # cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
    # cv2.imshow("Cat Faces", resizedImage)
    # cv2.waitKey(0)

