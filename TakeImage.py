from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import socket
import datetime
import numpy as np

ip = "140.112.94.128"
port = 13077
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
camera = PiCamera()
camera.resolution = (480,320)
camera.framerate = 32
camera.rotation = 180


d=datetime.datetime.now()
dx=d.strftime("%Y-%m-%d %H:%M:%S")
location="/var/www/html/images/"+dx+".jpg"
filename=dx+".jpg"

#sock.sendto(filename, (ip,port))

#print(location)
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture,format="bgr")
image = rawCapture.array


#cv2.imwrite(location,image)

cv2.imshow("Image",image)
cv2.waitKey(0)

