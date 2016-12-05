#!/bin/bash

sudo apt-get purge wolfram-engine
sudo apt-get clean
sudo apt-get autoremove

sudo apt-get remove --purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove