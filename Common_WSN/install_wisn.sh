#!/bin/bash

read -p "Install WiSN? Y/N  " -n 1 -r
echo
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
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
fi




echo "Please enter node number:"
read input_variable
echo "New node number: $input_variable"

cat > NODE_NUM.txt <<- EOF
    $input_variable
EOF

echo "Please enter DB number:"
read input_variable
echo "New DB number: $input_variable"

cat > DB_NUM.txt <<- EOF
    $input_variable
EOF




