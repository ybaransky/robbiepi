#!/usr/bin/env python

import time
import sys,traceback
import logging

def broken2():
	raise KeyError("this is carzy")

def broken():
	broken2()

try:
	for i in range(100):
		print i
		broken()
		time.sleep(2)
except Exception, Args:
#	print "caught ",Exception,Args
#	print repr(traceback.extract_tb(exc_traceback))
	logging.exception("caught it" + str(Args))


