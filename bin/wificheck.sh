#!/bin/bash

LOG_PATH="/var/log/etwork.log"
DATE=`date +%Y-%m-%d-%H:%M:%S`
TEST_IP=8.8.8.8
IFACE='wlan0'
LOGFILE=/home/pi/bin/act.log

# which interface to check
/bin/ping -c4 -I $IFACE $TEST_IP # 2>&1 > /dev/null
if [ $? != 0 ]
then
	echo $DATE "interface $IFACE broken, restarting" >> $LOGFILE
	sudo /sbin/shutdown -r
#	sudo ifdown --force $IFACE
#	sleep 5
#	sudo ifup $IFACE
#	sleep 5
#	sudo service ssh restart
else
	echo $DATE "interface $IFACE working" >> $LOGFILE
fi
