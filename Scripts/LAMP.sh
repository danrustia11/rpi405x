#!/bin/bash

# sudo chmod -R 755 /var/www/html

# sudo nano /etc/mysql/my.cnf
# --> change bind-ipaddress from 127.0.0.1 to 0.0.0.0
# sudo /etc/init.d/mysql restart

# sudo nano /etc/phpmyadmin/apache.conf
# --> add to the bottom Include /etc/phpymadmin/apache.conf

cd ~/
sudo apt-get install apache2 
sudo apt-get install php5
sudo apt-get install mysql-client mysql-server
sudo apt-get install tomcat6
sudo apt-get install vsftpd
sudo apt-get install phpmyadmin

