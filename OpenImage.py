import numpy as np
import cv2

cv2.__version__

img = cv2.imread('image.jpg',0)

cv2.imshow('display',img)
cv2.waitKey(0)
