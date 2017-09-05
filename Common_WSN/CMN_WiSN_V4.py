#!/usr/bin/python

#********************************#
#********************************#
#   Common platform WiSN program #
#    By: Dan Jeric Arcega Rustia #
#                                #
#   Log:                         #
#   8/29/2017 - txt file enable  #
#   8/3/2017 - added averaging   #
#   7/20/2017 - added image udp  #
#   7/5/2017 - added CSV backup  #
#   6/26/2017 - new program for  #
#               waterproof design#
#   5/22/2017 - removed com check#
#   5/12/2017 - added camera     #
#   5/5/2017 - added com check   #
#   3/30/2017 - finished up to   #
#               temp,hum and lux #
#             - udp sending      #
#********************************#
#********************************#

import subprocess
subprocess.call(['/home/pi/RPi_Cam_Web_Interface/stop.sh'])

#libraries
import time
import serial
import datetime
import socket

#cam libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import requests
import urllib2
from urllib import urlencode
import os

#sensor libraries
import Adafruit_DHT
import smbus
import csv


#############Options##############

#enable send to db server function
f = open('/home/pi/rpi405x/Common_WSN/DB_ENABLE.txt', 'r')
db_enable  = f.read()
db_enable = int(db_enable)

#node number (get from .txt file)
f = open('/home/pi/rpi405x/Common_WSN/NODE_NUM.txt', 'r')
node  = f.read()
node_num = int(node)
node = node.strip('\n')

f = open('/home/pi//rpi405x/Common_WSN/DB_NUM.txt', 'r')
db = f.read()
db = db.strip('\n')

#location
f = open('/home/pi//rpi405x/Common_WSN/LOCATION.txt', 'r')
location = f.read()
location = location.strip('\n')
location_cam = location+"_"+db

#enable sensors
s1 = 1
s2 = 1

#db codes where:
#PD=Pest detect
#BD=Bee detect
#PF=Plant factory
#CF=Cow farm
#H=Home envi
db_code = "PD"

dhtg = Adafruit_DHT.AM2302
dht_pin = 17

#sending delay in seconds
send_delay=360

#get data samples
gather_timer=12
gather_delay=12
samples=0
temp_samples=[0]*100
hum_samples=[0]*100
lux_samples=[0]*100

#csv backup filename
csv_filename="SENSOR_"+location_cam+"_"+node+".csv"

#################################
# Do not touch the codes below! #

#ip address and port
ip = "140.112.94.128"
port_udp = 20001
image_udp = 20002

# Open UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# file transfer url
url='http://140.112.94.128:10000/PEST_DETECT/PEST_IMAGES/RX_IMG.php?node='+node+'&location='+location_cam

# camera settings
camera = PiCamera()
camera.resolution = (3280,2464)
camera.framerate = 15
camera.rotation = 0
camera.awb_mode = 'auto'
camera.drc_strength = 'high'

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



####################
# Function Listing #
####################


def getImage():
    d=datetime.datetime.now()
    dx=d.strftime("%Y,%m,%d %H,%M,%S")
    
    print("Image captured!")
    locationx="/home/pi/PEST_IMAGES/"+dx+".jpg"
    print(locationx)
    filename=dx+".jpg"
    camera.capture(locationx)

    f = open(locationx,'rb')
    files = {'file':f}
    r=requests.post(url,files=files)
    print(r.content)
    


    # Send udp packet to image rx program
    # Sample: NODE3_2017,08,11 12,00,00.jpg:CHIAYI_GH_1:3:1:
    dx=d.strftime("%Y_%m_%d %H_%M_%S")
    filename=dx+".jpg"
    image_packet="NODE"+node+"_"+filename+":"+location+":"+node+":"+db+":"

    # Delay depending on node number:
    if db_enable==1:
        time.sleep(3*node_num)
        sock.sendto(image_packet, (ip,image_udp))
            


    # Send udp packet to image rx program
    # Sample: NODE3_2017,08,11 12,00,00.jpg:CHIAYI_GH_1:3:1:
    dx=d.strftime("%Y_%m_%d %H_%M_%S")
    filename=dx+".jpg"
    image_packet="NODE"+node+"_"+filename+":"+location+":"+node+":"+db+":"

    # Delay depending on node number:
    if db_enable==1:
        time.sleep(3*node_num)
        sock.sendto(image_packet, (ip,image_udp))
        print(image_packet)


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


getImage()

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
    gather_timer=gather_timer+1
    
    print("(TIMERS) Samples: " + str(samples) + \
          " Sensor: " + str(send_timer) + \
          "  Camera: " + str(hr) + ":" + str(mn) + ":" + str(sec)) + \
          " DB: " + str(db) + \
          " Node: " + str(node)
    time.sleep(1)


    # Data gathering function
    if gather_delay <= gather_timer:
        # Get hum temp reading
        hum, temp= Adafruit_DHT.read_retry(dhtg, dht_pin)

        # Get lux reading
        lux = readLight()

        # Put to arrays
        temp_samples[samples]=temp
        hum_samples[samples]=hum
        lux_samples[samples]=lux

                  
        print "(T) " + str(temp_samples[samples])
        print "(H) " + str(hum_samples[samples])
        print "(L) " + str(lux_samples[samples])
        

        if (temp_samples[samples] <= 50 and hum_samples[samples] <= 100 and hum_samples[samples] >= 30):
          samples=samples+1
        else:
          print "ERROR IN SENSOR READING!"
        gather_timer=0


    
    # Camera sending function
    if (mn == 10 and sec == 0) or (mn == 20 and sec == 0) or (mn == 30 and sec == 0) or (mn == 40 and sec == 0) or (mn == 50 and sec == 0) or (mn == 0 and sec == 0):
        if hr>6 and hr <=18:
            try:
                getImage()
            except:
                pass

    

    
    # Sensor data sending function
    if send_timer>=send_delay: 
        print("------------------------SEND DATA------------------------")

        # get sensor 1 data
        try:

            # get the average of sensors
            temp = sum(temp_samples)/samples
            hum = sum(hum_samples)/samples

            # get median
            #temp = statistics.median(temp_samples)
            #hum = statistics.median(hum_samples)

            # clear array
            temp_samples=[0]*100
            hum_samples=[0]*100

            # round off to two decimal places
            temp="{0:.2f}".format(temp)
            hum= "{0:.2f}".format(hum)
            
            if temp is not None and hum is not None:
                _packet1a=db_code+":ENVI:"+date_stamp+":"+node+":T:"+temp+":"+location+":"+db
                _packet1b=db_code+":ENVI:"+date_stamp+":"+node+":H:"+hum+":"+location+":"+db
                print(_packet1a)
                print(_packet1b)
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
            # get median
            lux = sum(lux_samples)/samples
            
            lux = "{0:.2f}".format(lux)
            _packet2a=db_code+":ENVI:"+date_stamp+":"+node+":L:"+lux+":"+location+":"+db
            print(_packet2a)
            text=[db_code,date_stamp,node,"L",lux,location,db]        
            with open(csv_filename, 'ab') as csv_file:
              writer = csv.writer(csv_file,delimiter=':')
              writer.writerow(text)
        except:
            pass

        send_timer=0
        samples=0


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

                port.reset_input_buffer()                        
            except:
                pass

        print("------------------------FINISHED SENDING------------------------")

             
            
      
