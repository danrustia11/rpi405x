#!/usr/bin/python

import sys
import time
import pigpio
import subprocess

# variables
myString="";
myExtract=[10]
outputA=""

# initialize gpios
RX=7 # UART receive pin
pi = pigpio.pi()
pi.exceptions= False
pi.set_mode(RX, pigpio.INPUT)


# open serial port
try:
    pi.bb_serial_read_open(RX,9600,8)
except:
    pi.bb_serial_read_close(RX)

pi.bb_serial_read_open(RX,9600,8)

    
while 1:
    #save data into bytearray
    (count, data) = pi.bb_serial_read(RX)
    try:
        if count>0:
            myString=data.decode("utf-8")
            print(myString)
            print(count)
            
    except:
         pass

                        
    time.sleep(1)
    
