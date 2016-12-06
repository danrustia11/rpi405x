#!/usr/bin/python

import sys
import time
import subprocess
import MySQLdb
import datetime


# open connection to database
# format: MySQLdb.connect("localhost","USERNAME","PASSWORD","DATABASE NAME")
try:
    conn = MySQLdb.connect("localhost","root","raspberry","testing_database")
except:
    print "ERROR CONNECTING!"

# make a cursor for DB connection
db = conn.cursor()

# get data and time
date = time.strftime("%Y-%m-%d")
clock = time.strftime("%H:%M")

# input data:
types = "TEMP"
value = 37.05
location = "MCDO"

command = """INSERT INTO Webserver1(DATE,TYPE,VALUE,LOCATION)VALUES('%s','%s',%s,'%s')""" % (date,types,value,location)
print command

try:
    db.execute(command)
    conn.commit()
    print "DATA SAVED!"
except:
    print "ERROR!"
    conn.rollback()


