import RPi.GPIO as GPIO
from math import exp,expm1
from sht1x.Sht1x import Sht1x as SHT1x
import time
GPIO.setwarnings(0)
datas = 17
clks = 4
sht1x = SHT1x(datas, clks, SHT1x.GPIO_BCM)



def READ():
    tempC = sht1x.read_temperature_C()
    temp = (9/5)*tempC+32
    print("Temperature: {}".format(tempC))
    hum = sht1x.read_humidity()
    hum = round(hum,2)
    print("Humidity: {}".format(hum))
    heat_index = -42.379+(2.04901523*temp)+(10.14333127*hum)-(0.22475541*temp*hum)-((6.83783*pow(10,-3))*temp*temp)-((5.481717*pow(10,-2))*hum*hum)+((1.22874*pow(10,-3))*hum*temp*temp)+((8.5282*pow(10,-4))*temp*hum*hum)-((1.99*pow(10,-6))*temp*temp*hum*hum)
    heat_index = round(heat_index,2)
    print("Heat index: {}".format(heat_index))
    time.sleep(30)
   
        
        
while True:
    READ()
