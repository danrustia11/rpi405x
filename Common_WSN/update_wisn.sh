#!/bin/bash

sudo rm -r /home/pi/rpi405x
cd
git clone https://github.com/danrustia11/rpi405x
cd /home/pi/rpi405x/Common_WSN
sudo chmod u+x *.sh

echo "Autorun which WSN/WiSN program? i.e. CMN_WiSN_USB.py"
echo "a: CMN_WiSN_USB.py - USB-based WiSN 2.0"
echo "b: CMN_WiSN_V4.py - WiSN 3.0 "
read input_file

if [ "$input_file" == "a" ] || [ "$input_file" == "A" ]; then
  input_variable="CMN_WiSN_USB.py"
elif [ "$input_file" == "b" ] || [ "$input_file" == "B" ]; then
  input_variable="CMN_WiSN_USB.py"
else
  echo "Please enter a letter!!"
  
echo "Autorun program: $input_variable"

cat > run_wisn.sh <<- EOF
#!/bin/bash
python /home/pi/rpi405x/Common_WSN/$input_variable
EOF




echo "Enable db sending? (0/1):"
read input_variable
echo "DB Enabled: $input_variable"
cat > DB_ENABLE.txt <<- EOF
$input_variable
EOF





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




echo "Please enter experiment location:"
read input_variable
echo "New experiment location: $input_variable"
cat > LOCATION.txt <<- EOF
$input_variable
EOF




sudo cp /home/pi/rpi405x/Common_WSN/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
