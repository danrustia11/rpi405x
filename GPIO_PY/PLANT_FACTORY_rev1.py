import RPi.GPIO as GPIO
from math import exp,expm1
from sht1x.Sht1x import Sht1x as SHT1x
import time
import socket
import subprocess
import random

# pin assignments
# SHT DAT = 11
# SHT CLK = 7
# DS18B20 DAT = 27

# define ip and port
TARGET_IP="140.112.94.129"
TARGET_PORT=13075
DB_NUMBER = "1:"

# delay in seconds
SENDING_DELAY = 300

# activate socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# disable gpio warnings from RPi.GPIO
GPIO.setwarnings(0)

# attach SHT1x
datas = 17
clks = 4
sht1x = SHT1x(datas, clks, SHT1x.GPIO_BCM)
hum = 0
temp = 0
temperature = 0
hum_string = ""
temp_string = ""
hi_string = ""
wtemp_string = ""

# udp string params
ID1 = "1:"
ID2 = "2:"
ID3 = "3:"
ID4 = "4:"
ID5 = "5:"
ID6 = "6:"
ID7 = "7:"
ID8 = "8:"
ID9 = "9:"
ID0 = "0:"

TYPET = "RT:"
TYPEH = "RH:"
TYPEHI = "HI:"
TYPEWT = "WT:"
TYPEWV = "WV:"


LOCATION = ":PF1:"
i = 0

def READ_DS18B20():
	# opens one wire of RPi
    my_file = open("/sys/bus/w1/devices/28-80000000d245/w1_slave")
    text = my_file.read()
    my_file.close() 
    # gets temp data from text
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature/1000
    wtemp_string = '%2.2f' %temperature
    return wtemp_string
    #print("Water Temperature: {} *C".format(temperature))

# obtain sensor values
def READ_SHT_T():	
    tempC = sht1x.read_temperature_C()
    temp = (9/5)*tempC+32
    #print("Temperature: {} *C".format(tempC))
    temp_string = '%2.2f' %tempC
    return temp_string
    
def READ_SHT_H():
	hum = sht1x.read_humidity()
	hum = round(hum,2)
	#print("Humidity: {} %RH".format(hum))
	hum_string = '%2.2f' %hum
	return hum_string

def READ_SHT_HI():
	# get temp and hum
	hum = sht1x.read_humidity()
	hum = round(hum,2)
	tempC = sht1x.read_temperature_C()
	temp = (9/5)*tempC+32
    
    # get heat index
	heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
	heat_indexC =(5*(heat_index-32))/9
	heat_index = round(heat_index,2)
	#print("Heat index: {} *C".format(heat_index))
	hi_string = '%2.2f' %heat_indexC
	return hi_string

def READ_WEIGHT(pot_number):
        # for testing:
        value = 10+(1.5+i*pot_number)
        weight_string = '%2.2f' %value
        return weight_string
    
while True:
	#FOR DEBUGGING:
    #READ_DS18B20()
    #READ_SHT_H()
    #READ_SHT_T()
    #READ_SHT_HI()
    i=i+1
    # save packets
    PACKET_H = ID0 + TYPEH + READ_SHT_H() + LOCATION + DB_NUMBER
    PACKET_T = ID0 + TYPET + READ_SHT_T() + LOCATION + DB_NUMBER
    PACKET_HI = ID0 + TYPEHI + READ_SHT_HI() + LOCATION + DB_NUMBER
    PACKET_WT = ID0 + TYPEWT + READ_DS18B20() + LOCATION + DB_NUMBER
    PACKET_W1 = ID1 + TYPEWV + READ_WEIGHT(1) + LOCATION + DB_NUMBER
    PACKET_W2 = ID2 + TYPEWV + READ_WEIGHT(2) + LOCATION + DB_NUMBER
    PACKET_W3 = ID3 + TYPEWV + READ_WEIGHT(3) + LOCATION + DB_NUMBER
    PACKET_W4 = ID4 + TYPEWV + READ_WEIGHT(4) + LOCATION + DB_NUMBER
    PACKET_W5 = ID5 + TYPEWV + READ_WEIGHT(5) + LOCATION + DB_NUMBER
    PACKET_W6 = ID6 + TYPEWV + READ_WEIGHT(6) + LOCATION + DB_NUMBER
    PACKET_W7 = ID7 + TYPEWV + READ_WEIGHT(7) + LOCATION + DB_NUMBER
    PACKET_W8 = ID8 + TYPEWV + READ_WEIGHT(8) + LOCATION + DB_NUMBER
    
    # check packets
    print(PACKET_H)
    print(PACKET_T)
    print(PACKET_HI)
    print(PACKET_WT)
    print(PACKET_W1)
    print(PACKET_W2)
    print(PACKET_W3)
    print(PACKET_W4)
    print(PACKET_W5)
    print(PACKET_W6)
    print(PACKET_W7)
    print(PACKET_W8)
    
    # send to db
    sock.sendto(PACKET_H, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_T, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_HI, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_WT, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W1, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W2, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W3, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W4, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W5, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W6, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W7, (TARGET_IP,TARGET_PORT))
    sock.sendto(PACKET_W8, (TARGET_IP,TARGET_PORT))
    
    
    # sample socket
    #sock.sendto("1:WV:5.12:PF1", (TARGET_IP,TARGET_PORT))
    time.sleep(SENDING_DELAY)

        

