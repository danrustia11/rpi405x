#!/usr/bin/python

#********************************#
#********************************#
#   Common platform WSN program  #
#   by: Dan Jeric Arcega Rustia  #
#                                #
#   Log:                         #
#   5/5/2017 - added com check   #
#   3/30/2017 - finished up to   #
#               temp,hum and lux #
#             - udp sending      #
#********************************#
#********************************#

#libraries
import time
import serial
import datetime
import socket

#############Options##############

#enable send to db server function
db_enable = 0

#db number
db = "1"

#node number
node = "1"

#location
location = "SHUIYUAN"

#db codes where:
#PD=Pest detect
#BD=Bee detect
#PF=Plant factory
#CF=Cow farm
#H=Home envi
db_code = "H"

#ip address and port
ip = "140.112.94.128"
port_udp = 20001

#enable sensor 1=on, 0=off
s1 = 1
s2 = 1
s3 = 0

#declare sensor code:
sensor1 = 'T' # Humidity+temperature
sensor2 = 'L' # Light intensity
sensor3 = 'P' # Pressure
check = 'x'   # communications check

#sending delay in seconds
send_delay=30
send_timer=0


string=""
port=serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#################################
# Do not touch the codes below! #

# Open UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Close and open serial port (resets the module)
port.close()
time.sleep(1)
port.open()
print("PROGRAM START")
print("TARGET IP:"+ip+" PORT:"+str(port_udp))
print("DB CODE:"+db_code+" NODE#"+node)

time.sleep(3)


def txrx(inputs):
    try:
        port.write(inputs)
        while port.inWaiting():
            try:
                time.sleep(0.01)
                reading = port.readline()
                return reading
            except:
                pass
        time.sleep(0.1)
    except:
        pass


def tx(inputs):
    try:
        port.write(inputs)
    except:
        pass

while 1:
   
    time_stamp = time.time()
    date_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H-%M-%S')
    #print(date_stamp)



    send_timer=send_timer+1
    print(send_timer)
 
    if send_timer < send_delay and send_timer>=0:
        tx(check)
        send_ok = 1
        time.sleep(1)

    

    if send_timer>=send_delay: 
        print("Querying...")
        if s1==1:

            # get sensor 1 data
            try:
                read1 = txrx(sensor1)
               # print(read1)
                if len(read1) > 10:
                    read1split=read1.split(' ')
                    r1a=read1split[0]
                    r1b=read1split[1]
                    r1c=read1split[2]
                    t1a=r1a[0:1]
                    t1b=r1b[0:1]
                    t1c=r1c[0:1]
                    v1a=r1a[2:10]
                    v1b=r1b[2:10]
                    v1c=r1c[2:10]
                    _packet1a=db_code+":"+date_stamp+":"+node+":"+t1a+":"+v1a+":"+location+":"+db
                    _packet1b=db_code+":"+date_stamp+":"+node+":"+t1b+":"+v1b+":"+location+":"+db
                    _packet1c=db_code+":"+date_stamp+":"+node+":"+t1c+":"+v1c+":"+location+":"+db
                    print(_packet1a)
                    print(_packet1b)
                    print(_packet1c)
                    send_timer=0
                    
            except:
                pass
            
            
            

        if s2==1:
            # get sensor 2 data
            try:
                read2 = txrx(sensor2)
                if len(read2) > 5:        
                    read2split=read2.split(' ')
                    r2a=read2split[0]
                    t2a=r2a[0:1]
                    v2a=r2a[2:12]
                    _packet2a=db_code+":"+date_stamp+":"+node+":"+t2a+":"+v2a+":"+location+":"+db
                    print(_packet2a)
            except:
                pass
                


        if db_enable==1:
            if s1==1 and len(read1)>10:
                sock.sendto(_packet1a, (ip,port_udp))
                sock.sendto(_packet1b, (ip,port_udp))
                sock.sendto(_packet1c, (ip,port_udp))
                
                
            if s2==1 and len(read2)>5:
                sock.sendto(_packet2a, (ip,port_udp))

         
        
  

  




