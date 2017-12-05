#!/usr/bin/env python

import os
import fnmatch
from time import sleep
from w1thermsensor import W1ThermSensor

class DS18B20Sensor():
	def __init__(self,id,name="",feed=""):
		self.type = "DS18B20"
		self.id = id
		self.feed = feed
		self.name = name
		self.sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,id)
		self.temperature = None
	def __str__(self):
		return str(	{'id' : self.id, 
					'type' : self.type,
					'feed' : self.feed, 
					'name' : self.name, 
					'temperature' : self.temperature} )
	def get_temperature(self):
		self.temperature = self.sensor.get_temperature(W1ThermSensor.DEGREES_F)
		return self.temperature

if __name__ == '__main__':
	try:
		# look for these in /sys/bus/w1/devices
		#sensor = TermperatureSensor("0316712980ff", "inside" )
		#sensor = TemperatureSensor("04167120acff", "inside" )
		# sensor = TemperatureSensor("031657211aff", "inside" )
		i=0
		sensors = []
		for file in os.listdir('/sys/bus/w1/devices'):
			if fnmatch.fnmatch(file,'28-*'):
				sensor = DS18B20Sensor(file[3:], "sensor-%d"%i)
				sensors.append(sensor)
				i += 1

		i = 0
		while True:
			for sensor in sensors:
				temp = sensor.get_temperature()
				print "%d name:%s id:%s %s temp:%0.2f" % \
					(i,sensor.name, sensor.id, sensor.type, sensor.temperature)
				i += 1
			sleep(2)
	finally:
		print "Good-bye"
