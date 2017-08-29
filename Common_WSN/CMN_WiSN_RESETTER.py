import RPi.GPIO as GPIO
import time
import urllib

GPIO.setmode(GPIO.BCM)

D1 = 2
D2 = 3
D3 = 17
D4 = 27

GPIO.setwarnings(False)

GPIO.setup(D1, GPIO.OUT)
GPIO.setup(D2, GPIO.OUT)
GPIO.setup(D3, GPIO.OUT)
GPIO.setup(D4, GPIO.OUT)

def turnOnSystem():
    GPIO.output(D1, 1)
    GPIO.output(D2, 1)
    GPIO.output(D3, 1)
    GPIO.output(D4, 1)
    time.sleep(1)

def turnOffSystem():
    GPIO.output(D1, 0)
    GPIO.output(D2, 0)
    GPIO.output(D3, 0)
    GPIO.output(D4, 0)
    time.sleep(5)

def checkWifi():
    try:
        url = "https://www.google.com"
        urllib.urlopen(url)
        status = "Connected"
    except:
        status = "Not connected"
        
    print status

    

    if status == "Connected":
        print "OK"
        turnOnSystem()
        
    if status == "Not connected":
        print "Restarting system..."
        turnOffSystem()
        turnOnSystem()
        time.sleep(60)

try:
    url = "https://www.google.com"
    urllib.urlopen(url)
except:
    pass

    
while 1:
    checkWifi()


    

    

