#!/usr/bin/env python

import time
import smbus2  # i used smbus2 at robbiepi
import bme280
from sensor import Sensor
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

class BME280Sensor(Sensor):

	def __init__(self,mode="unkown",location="unknown",feeds={},port=1,address=0x76):
		if not feeds:
			feeds = { 'temperature': None, 'pressure': None, 'humidity': None }
		data = {
				'temperature': {'value':None,'feed':feeds['temperature'],'units': "f"},
				'pressure':    {'value':None,'feed':feeds['pressure'],'units': "in-Hg"},
				'humidity':    {'value':None,'feed':feeds['humidity'],'units': "%"}
				}
		super(BME280Sensor, self).__init__("bme280",mode,location,data)
		self._port = port
		self._address = address
		self._bus = smbus2.SMBus(port)
		bme280.load_calibration_params(self._bus, address)

	def __str__(self):
		return super(BME280Sensor,self).__str__() + " "

	def humidity(self):
		self.sample()
		return self._data['humidity']['value']

	def pressure(self):
		self.sample()
		return self._data['pressure']['value']

	def sample(self):
		if (super(BME280Sensor,self).sample()):
			data = bme280.sample(self._bus, self._address)
			self._data['temperature']['value'] = data.temperature * 1.8 + 32.0 # Farenheit
			self._data['pressure']['value'] = data.pressure * 0.0295299714 # inches-Hg
			self._data['humidity']['value'] = data.humidity # %

	def send_to_adafruit(self, adafruit):
		for k,v in self._data.iteritems():
			feed = v['feed']
			value = v['value']
			units = v['units']
			super(BME280Sensor,self).send_to_adafruit(adafruit, feed, value, 
				"sending %s %s %s=%0.2f%s" % (self.model, self.location, k, value, units)
				)


if __name__ == '__main__':
	try:
		sensor = BME280Sensor("primary","outside")
		i=0
		while True:
			sensor.sample()
			sensor.send_to_adafruit(None)
			print i,sensor
			i = i+1
			time.sleep(2)
	finally:
		print "Good-bye"
