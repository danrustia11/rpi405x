#!/bin/sh

echo "Autorun which WSN/WiSN program? i.e. CMN_WiSN_USB.py"
read input_variable

cat > run_wisn.sh <<- EOF
    #!/bin/bash
        #!/bin/bash
    python /home/pi/rpi405x/Common_WSN/$input_variable
EOF

sudo cp /home/pi/rpi405x/Common_WSN/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
