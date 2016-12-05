from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket
import datetime
import numpy as np

ip = "140.112.94.128"
port = 13078
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
camera = PiCamera()
camera.resolution = (1312,976)
camera.framerate = 15
camera.rotation = 180
camera.awb_mode = 'fluorescent'
camera.drc_strength = 'high'

def takeImage():
    d=datetime.datetime.now()
    dx=d.strftime("%Y,%m,%d %H,%M,%S")
    location="/var/www/html/images/"+dx+".jpg"
    #location="/var/www/html/test/"+dx+".jpg"
    filename=dx+".jpg"
    
    #sock.sendto(filename, (ip,port))

    print(location)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture,format="bgr")
    image = rawCapture.array
    

    cv2.imwrite(location,image)
    #cv2.imshow("Image",image)

while 1:
    takeImage()
    time.sleep(1200)
