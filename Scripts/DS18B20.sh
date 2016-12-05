#!/bin/bash

sudo modprobe w1-gpio
sudo modprobe w1-therm
cd /sys/bus/w1/devices
ls


#change dtoverlay=w1.gpio,gpiopin=x in "sudo nano /boot/config.txt"
