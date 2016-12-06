import socket
import subprocess
import time

# define ip and port
TARGET_IP="192.168.0.4"
TARGET_PORT=1500

# activate socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
while True:
    sock.sendto("1:WV:5.12:PF1", (TARGET_IP,TARGET_PORT))
    time.sleep(10)
