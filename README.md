# Nexmo-Room-Monitoring

Hey!

The primary purpose of this project was to open the door to Computer Vision and test it out, and Im ust say, its been a great success.

This project will use an attached webcam and begin monitoring the room or area you set it for. If it detects any motion, itll take the frame that triggered it, and upload it to Imgur. Afterwards, it texts you a picture of the image so you can check it whereever you are.

In order to use this properly, please follow the directions below:

1. Install OpenCV2 for Python 2.7
2. Install Flask
3. Install imutils
4. Get a Nexmo API and Imgur API
5. Create .txt document anywhere you want and type the following. Make sure you have a space in between each one and its value. Essentially we want a space separate file, one item per line. Phone number needs to be (for US) 1##########
6. Ability to open a port of your choice. I set it to use port 65534. You also need to set your Nexmo callback for SMS receving to your `http://<IPADDRESS>:<PORT>`

    ```
    phoneNumber 1xxxxxxxxxx
    nexmoClientId xxxxxxxxxx
    nexmoClientSecret xxxxxxxxxx
    imgurClientId xxxxxxxxxx
    imgurClientSecret xxxxxxxxxx
    ```

7. When running the program, run 

    ```
    VideoMonitoring.py RequestServer.py -k APIKeys.txt
    ```

8. Go ahead and run VideoMonitoring.py as well.

Note: If you're not able to get any video, it probably means you need to change the video source on line 96 of VideoMonitoring.py

    webCam = cv2.VideoCapture(0)

Cycle through different numbers.
