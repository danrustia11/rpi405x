#!/bin/bash
cd /home/pi
wget https://pypi.python.org/packages/source/r/rpiSht1x/rpiSht1x-1.2.tar.gz
tar -xzf rpiSht1x-1.2.tar.gz
cd rpiSht1x-1.2
sudo python setup.py install
