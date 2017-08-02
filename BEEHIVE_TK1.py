#!/usr/bin/python

#********************************#
#********************************#
#   TK1 Common Platform Program  #
#    By: Dan Jeric Arcega Rustia #
#                                #
#   Log:                         #
#   8/1/2017 - reads UART Input  #
#              from RPi, then    #
#              sends to DB       #
#********************************#
#********************************#


import serial
import socket

#ip address and port
ip = "140.112.94.128"
port_udp = 20001

# Open UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Uart setting
ser = serial.Serial("/dev/ttyTHS0")
ser.baudrate=115200

while 1:
    reading = ser.readline().strip("\n")
    print reading
    sock.sendto(reading, (ip,port_udp))
