from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (1312, 976)
camera.framerate = 30
camera.rotation = 180
#camera.brightness = 75
camera.awb_mode = 'fluorescent'
camera.drc_strength = 'high'

#camera.led = False
rawCapture = PiRGBArray(camera, size=(1312, 976))


# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 
	# show the frame
	cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
	#cv2.resizeWindow('Frame',640,480)
	cv2.imshow("Frame", image)
	
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
