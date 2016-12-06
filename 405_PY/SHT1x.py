import RPi.GPIO as GPIO
from math import exp,expm1
from sht1x.Sht1x import Sht1x as SHT1x
import time
GPIO.setwarnings(0)
datas = 23
clks =18

datas2 = 7
clks2 = 8

#datas = 9
#clks = 10

sht1x = SHT1x(datas, clks, SHT1x.GPIO_BCM)
sht1xB = SHT1x(datas2, clks2, SHT1x.GPIO_BCM)



def READ():
    print("SENSOR1")
    tempC = sht1x.read_temperature_C()
    temp = (9/5)*tempC+32
    print("Temperature: {}".format(tempC))
    hum = sht1x.read_humidity()
    hum = round(hum,2)
    if hum <= 20:
        hum=100
    print("Humidity: {}".format(hum))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
    heat_index = round(heat_index,2)
    print("Heat index: {}".format(heat_index))
    if hum == 100:
        print "ERROR!"
    
    time.sleep(1)
    
def READ2():
    print("SENSOR2")
    tempC = sht1xB.read_temperature_C()
    temp = (9/5)*tempC+32
    print("Temperature: {}".format(tempC))
    hum = sht1xB.read_humidity()
    hum = round(hum,2)
    print("Humidity: {}".format(hum))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
    heat_index = round(heat_index,2)
    print("Heat index: {}".format(heat_index))
    time.sleep(1)
   
        
        
while True:
    READ()
    #READ2()
