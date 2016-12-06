import RPi.GPIO as GPIO
import time
#         0 1 2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
my_map = [3,5,7,11,13,15,19,21,23,26,24,22,18,16,12,10,8]

# set pin modes
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(0)
# set i/o modes
for x in range(0,17):
    GPIO.setup(my_map[x], GPIO.OUT)
    GPIO.output(my_map[x],1)

def LIGHT():
    for x in range(0,17):
        GPIO.output(my_map[x],0)
        time.sleep(0.2)  
    for x in range(0,17):
        GPIO.output(my_map[x],1)
        time.sleep(0.2)
        
        
while True:
    LIGHT()
