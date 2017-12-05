#!/usr/bin/env python

import time
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# base class for all sensors that can send to Adafruit
class Sensor(object):
	'''base class for any sensor object'''

	SAMPLE_INTERVAL_SECS = 1.0

	def __init__(self, model="generic", mode="unknown", location="unknown", data=None):
		self._model = model
		self._mode = mode
		self._location = location
		self._sample_time = 0
		self._data = data
		self._temperature = None

	def __str__(self):
		s = ""
		if self._data:
			for k, v in self._data.iteritems():
				s += "%s:{value:%s,feed:%s}" % (k,v['value'],v['feed']) + " "

		return "model:" + str(self.model) + " " + \
			"mode:" + str(self.mode) + " " + \
			"location:" + str(self.location) + " " + s

	@property
	def temperature(self):
		self.sample()
		return self._data['temperature']['value']

	@property
	def model(self):
		return self._model

	@property
	def mode(self):
		return self._mode

	@property
	def location(self):
		return self._location

	def sample(self) :
		now = time.time()
		if (now - self._sample_time < Sensor.SAMPLE_INTERVAL_SECS):
			return False
		self._sample_time = now
		return True	
	
	def send_to_adafruit(self,adafruit, feed, value, str):
		logging.info(str)
		if adafruit:
			adafruit.send(feed, "%0.2f" % value)
	
if __name__ == '__main__':
	try:
		sensor = Sensor()
		while True:
			print sensor 
			time.sleep(2)
	finally:
		print "Good-bye"
