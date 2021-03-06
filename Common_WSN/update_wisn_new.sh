#!/bin/bash

sudo rm -r /home/pi/rpi405x
cd
sudo rm rpi405x_linux.tar.gz
wget --no-check-certificate "https://bblabcloud.bime.ntu.edu.tw/remote.php/webdav/Dan405/rpi405x_linux.tar.gz" --http-user=dan_rustia --http-password=d05631006
tar -xvzf rpi405x_linux.tar.gz
cd /home/pi/rpi405x/Common_WSN
sudo chmod u+x *.sh


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
echo "a: NTU_GH"
echo "b: CHIAYI_GH"
read input_loc

if [ "$input_loc" == "a" ] || [ "$input_loc" == "A" ]; then
  input_variable="NTU_GH"
elif [ "$input_loc" == "b" ] || [ "$input_loc" == "B" ]; then
  input_variable="CHIAYI_GH"
else
  echo "Please enter a letter!!"
fi
  

echo "New experiment location: $input_variable"
cat > LOCATION.txt <<- EOF
$input_variable
EOF



echo "Autorun which WSN/WiSN program? i.e. CMN_WiSN_USB.py"
echo "a: CMN_WiSN_USB.py - USB-based WiSN 2.0"
echo "b: CMN_WiSN_V4.py - WiSN 3.0 with Qt SVM ML"
echo "c: CMN_WiSN_V5.py - WiSN 3.0 with Python Inception DL"
echo "d: CMN_WiSN_THLP_V1.py - WiSN 4.0 with BME280 TH sensor"
read input_file

if [ "$input_file" == "a" ] || [ "$input_file" == "A" ]; then
  input_variable="CMN_WiSN_USB.py"
  elif [ "$input_file" == "b" ] || [ "$input_file" == "B" ]; then
  input_variable="CMN_WiSN_V4.py"
  elif [ "$input_file" == "c" ] || [ "$input_file" == "C" ]; then
  input_variable="CMN_WiSN_V5.py"
  elif [ "$input_file" == "d" ] || [ "$input_file" == "D" ]; then
  input_variable="CMN_WiSN_THLP_V1.py"
else
  echo "Please enter a letter!!"
fi
  
echo "Autorun program: $input_variable"

cat > run_wisn.sh <<- EOF
#!/bin/bash
python /home/pi/rpi405x/Common_WSN/$input_variable
EOF


sudo cp /home/pi/rpi405x/Common_WSN/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
