#!/usr/bin/env python

import os
import sys
import time
import datetime

import const as CONST

class sample(object):

	def __init__(self,value):
		self._value = value

	def set(self,value):
		self._value = value

	@property
	def value(self):
		return self._value;

#	@value.setter
#	def value(self,value):
#		self._value = value;
	
def now():
	return datetime.datetime.now().strftime("%Y%m%d %H:%M:%S.%f")[:-3]

print now()
print time.strftime("%Y%m%d_%H%M")

print "argv[0]",sys.argv[0]
print "abspath",os.path.abspath( sys.argv[0] )
print "dirname",os.path.dirname( os.path.abspath(sys.argv[0]) )
print "basename",os.path.basename( sys.argv[0] )
inifile = os.path.abspath(sys.argv[0])[:-3] + ".ini"
print inifile

psw = ['hello']
if psw :
	print "this is wired...",psw

CONST.LOCATION = "hunter"
CONST.ITERATIONS = 54
print CONST

s = sample(13)
print s.value;

s.set(23)
print s.value;
