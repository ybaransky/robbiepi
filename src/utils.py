#!/usr/bin/env python
#from __future__ import print_function

import sys
import os.path
import urllib2
import time
import datetime 
import logging
# logging.getLogger(__name__).addHandler(logging.NullHandler())

class EST(datetime.tzinfo):
	def utcoffset(self, dt):
		return datetime.timedelta(hours=-5)
	def dst(self,dt):
		return datetime.timedelta(0)

def	now():
	return datetime.datetime.now(EST()).strftime("%Y%m%d %H:%M:%S.%f")[:-3]

def init_logging(logfile):
	if not os.path.exists(os.path.dirname(logfile)):
		raise FileError, "ERROR: directory not found for %s" % logfile

	logging.basicConfig(
		level=logging.DEBUG
		,format = '%(asctime)s [%(funcName)s][%(levelname)s] %(message)s'
		,datefmt = '%Y-%m-%d %H:%M:%S'
		,filename = logfile + "." + time.strftime("%Y%m%d_%H%M")
		,filemode = "w")

	# attach console stream (or is this stderr?)
	formatter = logging.Formatter(
		'%(asctime)s %(message)s'
		, datefmt='%H:%M:%S')
	console = logging.StreamHandler(sys.stdout)
	console.setLevel(logging.INFO)
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)
	
def putchar(str):
	sys.stdout.write(str[0])
	sys.stdout.flush()

def wait(seconds):
	k = 0
	for i in range(seconds/10):
		if ((i+1) % 6) == 0:
			k += 1
			if k > 9: k = 0
			c = str(k)
		else: 
			c = '.'	
		putchar(c)
		time.sleep(10)
	print ""  # for the newline

def	internet_connected():
	url = "http://www.google.com"
	logging.info("checking internet connectivity using %s",url)
	try:
		status = urllib2.urlopen(url, timeout=5)
		logging.info("reachable")
		return True
	except urllib2.URLError as err:
		return False

def	uptime():
	'''
	string represetation of days, hours, minutes, seconds since the pi started
	'''
	with open('/proc/uptime','r') as f:
		uptime_seconds = round(float(f.readline().split()[0]))
		return str(datetime.timedelta(seconds = uptime_seconds))


if __name__ == '__main__':
	try:
		for i in range(3):
			print i,now(),uptime()
			time.sleep(1)
	finally :
		print "bye..."

