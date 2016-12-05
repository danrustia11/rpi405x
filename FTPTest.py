import ftplib
import os

from ftplib import FTP

ftp = FTP()
ftp.connect('140.112.94.128',15000)
ftp.login(user='LAB405',passwd='LAB405')



file = open('image.jpg','rb')
ftp.storbinary('STOR image.jpg',file)
file.close()
ftp.close()
#file.close()
#session.quit()
