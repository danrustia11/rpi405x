#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo rpi-update -y
sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer -y

cd /home/pi
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
chmod u+x *.sh
./install.sh
cd /home/pi

git clone https://github.com/adafruit/Adafruit_Python_DHT.git
sudo apt-get install build-essential python-dev -y
cd Adafruit_Python_DHT
sudo python setup.py install
cd /home/pi

mkdir PEST_IMAGES


