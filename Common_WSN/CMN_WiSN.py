#!/usr/bin/python

#********************************#
#********************************#
#   Common platform WiSN program #
#   by: Dan Jeric Arcega Rustia  #
#                                #
#   Log:                         #
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

#############Options##############

#enable send to db server function
db_enable = 1

#db number
db = "7"

#node number
node = "1"

#location
location = "NTU_GH"
location_cam = "NTU_GH"+"_"+db

#db codes where:
#PD=Pest detect
#BD=Bee detect
#PF=Plant factory
#CF=Cow farm
#H=Home envi
db_code = "PD"

#enable sensor 1=on, 0=off
s1 = 1
s2 = 1
s3 = 0

#declare sensor code:
sensor1 = 'T' # Humidity+temperature
sensor2 = 'L' # Light intensity
sensor3 = 'P' # Pressure
check = 'x'   # communications check

#sending delay in seconds
send_delay=360

#################################
# Do not touch the codes below! #

#ip address and port
ip = "140.112.94.128"
port_udp = 20001

# Serial settings
string=""
port=serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
send_timer=0


# Open UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# file transfer url
url='http://140.112.94.128:20000/PEST_DETECT/PEST_IMAGES/RX_IMG.php?node='+node+'&location='+location_cam

# camera settings
camera = PiCamera()
camera.resolution = (3280,2464)
camera.framerate = 15
camera.rotation = 180
camera.awb_mode = 'auto'
camera.drc_strength = 'high'

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

def txrx(inputs):
    try:
        port.write(inputs)
        time.sleep(3)
        while port.inWaiting():
            try:
                time.sleep(0.01)
                reading = port.readline()
                return reading
            except:
                pass
        time.sleep(0.1)
    except:
        pass


def tx(inputs):
    try:
        port.write(inputs)
    except:
        pass




##################
# Initialization #
##################

# Close and open serial port (resets the module)
port.close()
time.sleep(1)
port.open()
print("PROGRAM START")
print("TARGET IP:"+ip+" PORT:"+str(port_udp))
print("DB CODE:"+db_code+" NODE#"+node)
send_timer=send_delay
time.sleep(1)

#os.system('./home/pi/RPi_Cam_Web_Interface/stop.sh')
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
    mn=int(mn)
    sec=int(sec)
    ###########################

    send_timer=send_timer+1
    print("sensor: " + str(send_timer) + "  camera: " + str(hr) + ":" + str(mn) + ":" + str(sec))
    time.sleep(1)

    if (mn == 10 and sec == 0) or (mn == 20 and sec == 0) or (mn == 30 and sec == 0) or (mn == 40 and sec == 0) or (mn == 50 and sec == 0) or (mn == 0 and sec == 0):
        if hr>6 and hr <=18:
            try:
                getImage()
            except:
                pass

    if send_timer>=send_delay: 
        print("Querying...")
        if s1==1:

            # get sensor 1 data
            try:
                read1 = txrx(sensor1)
               # print(read1)
                if len(read1) > 10:
                    read1split=read1.split(' ')
                    r1a=read1split[0]
                    r1b=read1split[1]
                    r1c=read1split[2]
                    t1a=r1a[0:1]
                    t1b=r1b[0:1]
                    t1c=r1c[0:1]
                    v1a=r1a[2:10]
                    v1b=r1b[2:10]
                    v1c=r1c[2:10]
                    _packet1a=db_code+":"+date_stamp+":"+node+":"+t1a+":"+v1a+":"+location+":"+db
                    _packet1b=db_code+":"+date_stamp+":"+node+":"+t1b+":"+v1b+":"+location+":"+db
                    _packet1c=db_code+":"+date_stamp+":"+node+":"+t1c+":"+v1c+":"+location+":"+db
                    print(_packet1a)
                    print(_packet1b)
                    print(_packet1c)
                   
                    
            except:
                pass
            
            
            

        if s2==1:
            # get sensor 2 data
            try:
                read2 = txrx(sensor2)
                if len(read2) > 5:        
                    read2split=read2.split(' ')
                    r2a=read2split[0]
                    t2a=r2a[0:1]
                    v2a=r2a[2:12]
                    _packet2a=db_code+":"+date_stamp+":"+node+":"+t2a+":"+v2a+":"+location+":"+db
                    print(_packet2a)
            except:
                pass

        send_timer=0       


        if db_enable==1:
            try:
                if s1==1 and len(read1)>10:
                    sock.sendto(_packet1a, (ip,port_udp))
                    sock.sendto(_packet1b, (ip,port_udp))
                    sock.sendto(_packet1c, (ip,port_udp))
 
                    
                if s2==1 and len(read2)>5:
                    sock.sendto(_packet2a, (ip,port_udp))

                port.reset_input_buffer()                        
            except:
                pass

             
            
      

  




