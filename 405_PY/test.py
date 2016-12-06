import RPi.GPIO as GPIO
import time

# set pin modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)
# set i/o modes

GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)


def LIGHT():
        GPIO.output(7,0)
        GPIO.output(8,0)
        time.sleep(0.2)  
        GPIO.output(7,1)
        GPIO.output(8,1)
        time.sleep(0.2)
        
        
while True:
    LIGHT()
