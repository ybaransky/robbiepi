#!/usr/bin/env python

import time
import logging
from w1thermsensor import W1ThermSensor
from sensor import Sensor

logging.getLogger(__name__).addHandler(logging.NullHandler())

class DS18B20Sensor( Sensor ):

	def __init__(self, mode="primary", location="unknown", feeds = {'temperature':None}, serial=""):
		data = {'temperature': {'value':None, 'feed':feeds['temperature'], 'units': "f"} }
		super(DS18B20Sensor, self).__init__("ds18b20", mode, location, data)
		self._serial = serial
		self._sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,serial)

	def __str__(self):
		return super(DS18B20Sensor, self).__str__() + " " + \
			"serial:" + str(self._serial) + " " 

	@property
	def temperature(self):
		self.sample()
		return self._data['temperature']['value']

	def sample(self):
		# only sampel every so often
		if (super(DS18B20Sensor,self).sample()):
			self._data['temperature']['value'] = \
				self._sensor.get_temperature(W1ThermSensor.DEGREES_F)

	def send_to_adafruit(self,adafruit,data=None):
		k = 'temperature'
		feed = self._data[k]['feed']
		value = self._data[k]['value']
		units = self._data[k]['units']
		if data :
			k = "delta"
			value = data
	
		super(DS18B20Sensor, self).send_to_adafruit(adafruit, feed, value, 
			"sending %s %s %11s=%0.2f%s" % (self.model, self.location, k, value, units)
				)

def find_sensor_serial_numbers():
	import os
	import fnmatch
	serials = []
	for file in os.listdir('/sys/bus/w1/devices'):
		if fnmatch.fnmatch(file,'28-*'):
			serials.append(file[3:])
	return serials

if __name__ == '__main__':
	try:
		# look for these in /sys/bus/w1/devices
		sensors = []
		for i,serial in enumerate(find_sensor_serial_numbers()) :
			print "found ds18b20 sensor serial=%s" % serial
			sensor = DS18B20Sensor("primary","sensor-%d"%i, {'temperature':i}, serial)
			sensors.append(sensor)

		i=0
		while True:
			for sensor in sensors:
				sensor.sample()
				sensor.send_to_adafruit(None)
				print i,sensor
				i+=1
			time.sleep(2)
	finally:
		print "Good-bye"
