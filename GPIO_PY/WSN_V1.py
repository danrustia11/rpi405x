# Library imports
import RPi.GPIO as GPIO
from math import exp,expm1
from sht1x.Sht1x import Sht1x as SHT1x
import socket
import subprocess
import time

# define db params
DB_ID = "11"
HIVEA = "1A"
HIVEB = "1B"

# define ip and port
TARGET_IP="140.112.94.128"
TARGET_PORT=13076

# activate socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Remove GPIO warnings
GPIO.setwarnings(0)

# Pin outs
# Port1
datas = 22
clks = 27
# Port2
datas2 =9
clks2 = 10
# Port3
datas3 = 9
clks3 = 10

sht1x = SHT1x(datas, clks, SHT1x.GPIO_BCM)
sht1xB = SHT1x(datas2, clks2, SHT1x.GPIO_BCM)
sht1xC = SHT1x(datas3, clks3, SHT1x.GPIO_BCM)



def READ():
    print("SENSOR1")
    tempC = sht1x.read_temperature_C()
    temp = (9/5)*tempC+32
    print("Temperature: {}".format(tempC))
    hum = sht1x.read_humidity()
    hum = round(hum,2)
    print("Humidity: {}".format(hum))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
    heat_index = round(heat_index,2)
    print("Heat index: {}".format(heat_index))
    output = HIVEA+":"+str(tempC)+":"+str(hum)+":0:"+DB_ID
    print(output)
    sock.sendto(output, (TARGET_IP,TARGET_PORT))
    
def READ2():
    print("SENSOR2")
    tempC = sht1xB.read_temperature_C()
    temp = (9/5)*tempC+32
    print("Temperature: {}".format(tempC))
    hum2 = sht1xB.read_humidity()
    hum2 = round(hum2,2)
    if hum2<=0:
        hum2 = sht1x.read_humidity()
        hum2 = round(hum2,2)
    print("Humidity: {}".format(hum2))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum2)-(0.22475541*temp*hum2)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum2*hum2)+((1.22874*pow(10,-3))*hum2*temp*temp)+((8.5282*pow(10,-4))*temp*hum2*hum2)-((1.99*pow(10,-6))*temp*temp*hum2*hum2)
    heat_index = round(heat_index,2)
    print("Heat index: {}".format(heat_index))
    output = HIVEB+":"+str(tempC)+":"+str(hum2)+":0:"+DB_ID
    print(output)
    sock.sendto(output, (TARGET_IP,TARGET_PORT))
   
        
        
while True:
    READ()
    READ2()
    time.sleep(360)
