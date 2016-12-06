#!/usr/bin/python

import sys
import time
import pigpio
import subprocess
import MySQLdb
import datetime

# variables
myString="";
myExtract=[10]
outputA=""

# initialize gpios
RX=7 # UART receive pin
pi = pigpio.pi()
pi.exceptions= False
pi.set_mode(RX, pigpio.INPUT)

# open connection to database
# format: MySQLdb.connect("localhost","USERNAME","PASSWORD","DATABASE NAME")
try:
    conn = MySQLdb.connect("localhost","root","raspberry","testing_database")
except:
    print "ERROR CONNECTING!"
db = conn.cursor()

# get date
date = time.strftime("%Y-%m-%d")

# open serial port
try:
    pi.bb_serial_read_open(RX,9600,8)
except:
    pi.bb_serial_read_close(RX)

pi.bb_serial_read_open(RX,9600,8)

def insertData(str):
    print str
    try:
        db.execute(str)
        conn.commit()
        print "DATA SAVED!"
    except:
        print "ERROR!"
        conn.rollback()

    
while 1:
    #save data into bytearray
    (count, data) = pi.bb_serial_read(RX)
    try:
        if count >= 30:
            #bytearray to string
            myString=data.decode("utf-8")
            
            #split string
            myExtract=myString.split(",")
            header=myExtract[0]
            altitude=myExtract[1]
            pressure=myExtract[2]
            temperature=myExtract[3]
            lux=myExtract[4]
            rain1=myExtract[5]
            rain2=myExtract[6]
            footer=myExtract[7]

            types1 = "PRESSURE"
            types2 = "TEMP"
            types3 = "LIGHT"

            value1=pressure
            value2=temperature
            value3=lux

            location = "MCDO"

            command1 = """INSERT INTO Webserver1(DATE,TYPE,VALUE,LOCATION)
                                        VALUES('%s','%s',%s,'%s')""" % (date,types1,value1,location)
            command2 = """INSERT INTO Webserver1(DATE,TYPE,VALUE,LOCATION)
                                        VALUES('%s','%s',%s,'%s')""" % (date,types2,value2,location)
            command3 = """INSERT INTO Webserver1(DATE,TYPE,VALUE,LOCATION)
                                        VALUES('%s','%s',%s,'%s')""" % (date,types3,value3,location)            
            
            insertData(command1)
            insertData(command2)
            insertData(command3)

          
                        
    except:
         pass

                        
    time.sleep(1)


    
