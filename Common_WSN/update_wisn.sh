#!/bin/bash

sudo rm -r /home/pi/rpi405x
cd
git clone https://github.com/danrustia11/rpi405x
cd /home/pi/rpi405x/Common_WSN
sudo chmod u+x *.sh


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


echo "Autorun which WSN/WiSN program? i.e. CMN_WiSN_USB.py"
read input_variable

cat > run_wisn.sh <<- EOF
#!/bin/bash
python /home/pi/rpi405x/Common_WSN/$input_variable
EOF
