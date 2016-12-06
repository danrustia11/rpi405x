#!/usr/bin/python

# libraries
import pigpio

# initialize gpios
pi = pigpio.pi()
pi.exceptions= False

for i in range(0,32):
    print("gpio {} is {}".format(i,pi.read(i)))
          
