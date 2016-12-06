import socket
import subprocess
import time

# define ip and port
TARGET_IP="140.112.94.129"
TARGET_PORT=13075

# activate socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
while True:
    sock.sendto("1:WV:5.12:PF1", (TARGET_IP,TARGET_PORT))
    time.sleep(10)
