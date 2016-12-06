#!/usr/bin/python

import sys
import time
import difflib
import pigpio
import socket
import subprocess

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# define ip and port
TARGET_IP="140.112.94.128"
TARGET_PORT=13077

RX=23
myString="";
myExtract=[10]
HIVE="1"
DB_ID="11"
counter=0
output=""

pi = pigpio.pi()
pi.exceptions= False

pi.set_mode(RX, pigpio.INPUT)

try:
    pi.bb_serial_read_open(RX, 9600, 8)
except:
    pi.bb_serial_read_close(RX)

pi.bb_serial_read_open(RX, 9600, 8)

while 1:
    (count, data) = pi.bb_serial_read(RX)
    counter = counter+1
    waiting = "Elapsed time:"+str(counter)+" Count:"+str(count)+" Latest output:"+str(output)
    print waiting
    if count >= 35:
        #get data in bytearray
        print data

        #bytearray to string
        myString=data.decode("utf-8")
        
        #split string
        myExtract=myString.split(",")
        print type(myExtract[7])
        print myExtract[7]


        header=myExtract[0]
        altitude=myExtract[1]
        pressure=myExtract[2]
        temperature=myExtract[3]
        lux=myExtract[4]
        rain1=myExtract[5]
        rain2=myExtract[6]
        footer=myExtract[7]
        counter=0
    
        print("HEADER:"+header)
        print("ALTITUDE:"+altitude)
        print("PRESSURE:"+pressure)
        print("TEMPERATURE:"+temperature)
        print("LUX:"+lux)
        print("RAIN1:"+rain1)
        print("RAIN2:"+rain2)
        print("FOOTER:"+footer)
        output=HIVE+":"+str(altitude)+":"+str(pressure)+":"+str(temperature)+":"+str(lux)+":"+str(rain1)+":"+str(rain2)+":"+DB_ID
        print(output)
        sock.sendto(output, (TARGET_IP,TARGET_PORT))


                        
    time.sleep(1)

