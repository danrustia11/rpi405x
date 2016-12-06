#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import time
import difflib
import pigpio
import socket
import subprocess

from math import exp,expm1
from sht1x.Sht1x import Sht1x as SHT1x

# define db params
HIVE="2"
DB_ID = "12"
HIVEA = "2A"
HIVEB = "2B"
RX=25

# Pin outs
# Port1
datas = 18
clks = 23
# Port2
datas2 = 9
clks2 = 10

# variables
myString="";
myExtract=[10]
outputA=""
outputB=""
outputC=""
counter=0

# define ip and port
TARGET_IP="140.112.94.128"
TARGET_PORT=13077
TARGET_PORT2=13076

# activate socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Remove GPIO warnings
GPIO.setwarnings(0)

# initialize gpios
sht1x = SHT1x(datas, clks, SHT1x.GPIO_BCM)
sht1xB = SHT1x(datas2, clks2, SHT1x.GPIO_BCM)
pi = pigpio.pi()
pi.exceptions= False
pi.set_mode(RX, pigpio.INPUT)

try:
    pi.bb_serial_read_open(RX,9600,8)
except:
    pi.bb_serial_read_close(RX)

pi.bb_serial_read_open(RX,9600,8)


def READ2():
    #print("SENSOR1")
    tempC = sht1x.read_temperature_C()
    temp = (9/5)*tempC+32
    #print("Temperature: {}".format(tempC))
    hum = sht1x.read_humidity()
    hum = round(hum,2)
    #print("Humidity: {}".format(hum))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
    heat_index = round(heat_index,2)
    #print("Heat index: {}".format(heat_index))
    READ2.outputB = HIVEA+":"+str(tempC)+":"+str(hum)+":0:"+DB_ID
    #print(output)
    
def READ3():
    #print("SENSOR2")
    tempC = sht1xB.read_temperature_C()
    if tempC >= 80:
        tempC=sht1x.read_temperature_C()
    temp = (9/5)*tempC+32
    #print("Temperature: {}".format(tempC))
    hum = sht1xB.read_humidity()
    if hum <= 0:
        hum=sht1x.read_humidity()
    hum = round(hum,2)
    #print("Humidity: {}".format(hum))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
    heat_index = round(heat_index,2)
    #print("Heat index: {}".format(heat_index))
    READ3.outputC = HIVEB+":"+str(tempC)+":"+str(hum)+":0:"+DB_ID
    #print(output)

    
while 1:
    (count, data) = pi.bb_serial_read(RX)
    counter = counter+1
    #waiting = "Elapsed time:"+str(counter)+" out:"+str(outputA)
    #print waiting
    try:
        if count >= 30:
            #get data in bytearray
            #print data

            #bytearray to string
            myString=data.decode("utf-8")
            
            #split string
            myExtract=myString.split(",")
            header=myExtract[0]
            altitude=myExtract[1]
            pressure=myExtract[2]
            temperature=myExtract[3]
            lux=myExtract[4]
            rain1=myExtract[5]
            rain2=myExtract[6]
            footer=myExtract[7]
            counter=0

            #print("HEADER:"+header)
            #print("ALTITUDE:"+altitude)
            #print("PRESSURE:"+pressure)
            #print("TEMPERATURE:"+temperature)
            #print("LUX:"+lux)
            #print("RAIN1:"+rain1)
            #print("RAIN2:"+rain2)
            #print("FOOTER:"+footer)

            outputA=HIVE+":"+str(altitude)+":"+str(pressure)+":"+str(temperature)+":"+str(lux)+":"+str(rain1)+":"+str(rain2)+":"+DB_ID

            READ2()
            #READ3()
            print(outputA)
            #print(READ2.outputB)
            #print(READ3.outputC)
            #sock.sendto(outputA, (TARGET_IP,TARGET_PORT))
            #sock.sendto(READ2.outputB, (TARGET_IP,TARGET_PORT2))
            #sock.sendto(READ3.outputC, (TARGET_IP,TARGET_PORT2))
    except:
         pass

                        
    time.sleep(1)
    
