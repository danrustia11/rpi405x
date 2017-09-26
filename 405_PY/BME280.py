import bme280
import time
import smbus

port = 1
address = 0x76
bus = smbus.SMBus(port)

bme280.load_calibration_params(bus, address)

while 1:

    data = bme280.sample(bus, address)
    t = round(data.temperature,2)
    h = round(data.humidity,2)
    p = round(data.pressure,2)
    
    
    print(t)
    print(h)
    print(p)



    time.sleep(5)
