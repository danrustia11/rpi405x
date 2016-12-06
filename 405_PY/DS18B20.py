import RPi.GPIO as GPIO
import time


def READ_WTEMP():
    my_file = open("/sys/bus/w1/devices/28-80000000d245/w1_slave")
    text = my_file.read()
    my_file.close() 
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature/1000
    print temperature
    time.sleep(3)
    
        
while True:
    READ()
