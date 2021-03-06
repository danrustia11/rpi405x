#!/usr/bin/python

#********************************#
#********************************#
#   Common platform WSN program #
#    By: Dan Jeric Arcega Rustia #
#                                #
#   Log:                         #
#   8/1/2017 - reads db and node #
#             from txt file      #
#            - added serial send #
#             to TK1             #
#            - optionally, can   #
#             send independently #
#             by setting         #
#             db_enable = 1      #
#********************************#
#********************************#

import subprocess

#libraries
import time
import serial
import datetime
import socket

import numpy as np
import requests
import urllib2
from urllib import urlencode
import os

#sensor libraries
import Adafruit_DHT
import smbus
import csv

import serial

#############Options##############

#enable send to db server function
db_enable = 0

#db number
db = "10"

#node number (get from .txt file)
f = open('/home/pi/rpi405x/Common_WSN/NODE_NUM.txt', 'r')
node  = f.read()
node = node.strip('\n')
node_num = int(node)

f = open('/home/pi/rpi405x/Common_WSN/DB_NUM.txt', 'r')
db  = f.read()
db = db.strip('\n')

#location
location = "HSINCHU"
location_cam = "HSINCHU"+"_"+db

#enable sensors
s1 = 1
s2 = 1
s3 = 1

#db codes where:
#PD=Pest detect
#BD=Bee detect
#PF=Plant factory
#CF=Cow farm
#H=Home envi
db_code = "BD"

dhtg = Adafruit_DHT.AM2302
dht_pin = 17
dht_pin2 = 27

#sending delay in seconds
send_delay=5

#csv backup filename
csv_filename="SENSOR_"+location_cam+"_"+node+".csv"

#################################
# Do not touch the codes below! #

#ip address and port
ip = "140.112.94.128"
port_udp = 20021

# Open UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Open UART
ser = serial.Serial("/dev/ttyS0")
ser.baudrate=115200

#bh1750 constants
DEVICE     = 0x23 # Default device I2C address
 
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
 
# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23
 
#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)


##################
# Initialization #
##################

# Close and open serial port (resets the module)
print("PROGRAM START")
print("TARGET IP:"+ip+" PORT:"+str(port_udp))
print("DB CODE:"+db_code+" NODE#"+node)
print("BACK-UP CSV:"+"SENSOR_"+location_cam+"_"+node+".csv")


# Make back-up csv file
fileexist = os.path.isfile(csv_filename)
text=['DB_CODE','DATE','NODE','TYPE','VALUE','LOCATION','DB']

if fileexist:      
  print("BACK-UP CSV ALREADY EXISTS!")
else:
  file = open(csv_filename, 'w')
  with open(csv_filename, 'ab') as csv_file:
    writer = csv.writer(csv_file,delimiter=':')
    writer.writerow(text)
  
send_timer=send_delay
time.sleep(1)


##################
#       END      #
##################

while 1:

    ##########################
    #### GET TIME AND DATE ###

    # DT format for sensors
    time_stamp = time.time()
    date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H-%M-%S')

    # DT format for camera
    d=datetime.datetime.now()
    dx=d.strftime("%Y,%m,%d %H,%M,%S")

    hr=d.strftime("%H")
    mn=d.strftime("%M")
    sec=d.strftime("%S")

    hr=int(hr)
    mn = int (mn)
    sec = int (sec)
    ###########################

    send_timer=send_timer+1
    print("(TIMERS) Sensor: " + str(send_timer))
    time.sleep(1)

    if send_timer>=send_delay: 
        print("Querying...")

        # get sensor 1 data
        try:
            # read sensor data
            hum, temp= Adafruit_DHT.read_retry(dhtg, dht_pin)

            # round off to two decimal places
            temp="{0:.2f}".format(temp)
            hum= "{0:.2f}".format(hum)
            if temp is not None and hum is not None:
                _packet1a=db_code+":ENVI:"+date_stamp+":"+node+":T_IN:"+temp+":"+location+":"+db
                _packet1b=db_code+":ENVI:"+date_stamp+":"+node+":H_IN:"+hum+":"+location+":"+db
                print(_packet1a)
                print(_packet1b)
                ser.write(_packet1a+"\n")
                ser.write(_packet1b+"\n")
                text=[db_code,date_stamp,node,"T",temp,location,db]
                text2=[db_code,date_stamp,node,"H",hum,location,db]                
                with open(csv_filename, 'ab') as csv_file:
                  writer = csv.writer(csv_file,delimiter=':')
                  writer.writerow(text)
                  writer.writerow(text2)
        except:
            pass

        # get sensor 2 data
        try:
            # read sensor data
            hum, temp= Adafruit_DHT.read_retry(dhtg, dht_pin2)

            # round off to two decimal places
            temp="{0:.2f}".format(temp)
            hum= "{0:.2f}".format(hum)
            if temp is not None and hum is not None:
                _packet2a=db_code+":ENVI:"+date_stamp+":"+node+":T_OUT:"+temp+":"+location+":"+db
                _packet2b=db_code+":ENVI:"+date_stamp+":"+node+":H_OUT:"+hum+":"+location+":"+db
                print(_packet2a)
                print(_packet2b)
                ser.write(_packet2a+"\n")
                ser.write(_packet2b+"\n")
                text=[db_code,date_stamp,node,"T",temp,location,db]
                text2=[db_code,date_stamp,node,"H",hum,location,db]                
                with open(csv_filename, 'ab') as csv_file:
                  writer = csv.writer(csv_file,delimiter=':')
                  writer.writerow(text)
                  writer.writerow(text2)
        except:
            pass
        
            
        # get sensor 3 data
        try:
            lux = readLight()
            lux = "{0:.2f}".format(lux)
            _packet3a=db_code+":ENVI:"+date_stamp+":"+node+":L:"+lux+":"+location+":"+db
            print(_packet3a)
            ser.write(_packet3a+"\n")
            text=[db_code,date_stamp,node,"L",lux,location,db]        
            with open(csv_filename, 'ab') as csv_file:
              writer = csv.writer(csv_file,delimiter=':')
              writer.writerow(text)
        except:
            pass

        send_timer=0 

              


        if db_enable==1:
            try:
                if s1==1:
                    sock.sendto(_packet1a, (ip,port_udp))
                    time.sleep(0.2)
                    sock.sendto(_packet1b, (ip,port_udp))
                    time.sleep(0.2)
                    
                if s2==1:
                    sock.sendto(_packet2a, (ip,port_udp))
                    time.sleep(0.2)
                    sock.sendto(_packet2b, (ip,port_udp))
                    time.sleep(0.2)
                    
                if s3==1:
                    sock.sendto(_packet3a, (ip,port_udp))
                    time.sleep(0.2)


                port.reset_input_buffer()                        
            except:
                pass
