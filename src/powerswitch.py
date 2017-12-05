#!/usr/bin/env python

import time
import datetime
import RPi.GPIO as GPIO

class PowerSwitch(object):
	_PIN = 23
	def __init__(self, low=10, high=35):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PowerSwitch._PIN, GPIO.OUT)
		GPIO.output(PowerSwitch._PIN, False)
		self.enabled = False
		self.start_time = None
		self.end_time = None
		self.low = low
		self.high = high
	def enable(self, value=None):
		if value != None:
			GPIO.output(PowerSwitch._PIN, value)
			self.enabled = value
			if value:
				self.start_time = datetime.datetime.now()
			else:
				self.end_time = datetime.datetime.now()
		return self.enabled
	def process_temperature(temperature):
		changed = False
		if temperature > self.high:
			if self.enable():
				self.enable(False)
				changed = True
		elif temperature < self.low:
			if not self.enable():
				self.enable(True)
				changed = True
		return changed
	def elapsed_time(self):
		if self.end_time == self.start_time:
			return "0"
		return str(self.end_time - self.start_time)
	def cleanup(self):
		GPIO.cleanup()
	def __str__(self):
		return ( "enabled=" + str(self.enabled) + ","
			+ " low=" + str(self.low) + ","
			+ " high=" + str(self.high) + ","
			)
		
if __name__ == '__main__':
	pws = PowerSwitch()
	print "PowerSwitch: ",pws
	try:
		print "switch is ",pws.enable()
		while True:
			pws.enable(True)
			print "switch is ",pws.enable()
			time.sleep(5)
	finally:
		print "cleaing up"
		pws.cleanup()
