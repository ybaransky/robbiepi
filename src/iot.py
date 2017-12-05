#!/usr/bin/env python

import sys, os
import utils
import time
import logging
import const as CONST
from gmail import GMail
from powerswitch import PowerSwitch
from ConfigParser import SafeConfigParser
from Adafruit_IO import Client as AdafruitIOClient
from Adafruit_IO import AdafruitIOError
from ds18b20sensor import DS18B20Sensor
from bme280sensor import BME280Sensor
 
def init_logging():
	logfile = os.path.abspath(sys.argv[0])[:-3] + ".log"
	utils.init_logging(logfile)
	logging.info("logfile %s" % logfile)
	
def init_inifile():
	inifile = os.path.abspath(sys.argv[0])[:-3] + ".ini"
	logging.info("inifile %s" % inifile)
	parser = SafeConfigParser()
	parser.read(inifile)
	return parser

def init_adafruit(parser):
	# create the Adafruit-io feeds
	key = parser.get("adafruit-io","key")
	aio = AdafruitIOClient(key)
	logging.info("aiokey %s %s" % (key,aio))
	return aio

def init_sensors(parser):
	sensors = []
	section = "sensors"
	count = parser.getint(section, "count")
	for i in range(count):
		section = "sensor-%d"%i
		mode = parser.get(section, "mode")
		model = parser.get(section, "model")
		location = parser.get(section, "location")
		if model == "bme280":
			feed_t = parser.get(section, "feed_t")
			feed_p = parser.get(section, "feed_p")
			feed_h = parser.get(section, "feed_h")
			feeds = {'temperature':feed_t,'pressure':feed_p,'humidity':feed_h}
			sensor = BME280Sensor(mode, location, feeds)
		else:
			serial = parser.get(section, "serial")
			feed_t = parser.get(section, "feed_t")
			sensor = DS18B20Sensor(mode, location, {'temperature':feed_t}, serial)
		logging.info("sensor %d) %s" % (i,str(sensor)))
		sensors.append( sensor )
	return sensors

def init_power_switch(parser):
	# hi and low temperature seetings for power logic
	powerswitch = None
	if parser.getboolean("powerswitch", "installed") :
		high = parser.getint("powerswitch", "high")
		low  = parser.getint("powerswitch", "low")
		powerswitch  = PowerSwitch(low, high)
	logging.info("powerswitch %s" % powerswitch)
	return powerswitch

def init_gmail(parser):
	email    = parser.get("gmail", "email")
	password = parser.get("gmail", "password")
	enabled  = parser.getboolean("gmail", "enabled")
	subject  = os.uname()[1]
	gm = GMail(email, password, subject, enabled);
	logging.info("gmail %s" % gm)
	return gm

def init_parameters(parser):
	CONST.MAX_ITERATIONS = parser.getint("parameters", "max_iterations")
	CONST.MEASUREMENT_INTERVAL = \
		parser.getint("parameters", "measurement_interval")
	logging.info("parameters %s" % CONST )
	return CONST

def find_sensor(mode, location):
	for sensor in sensors:   # this better be in order
		if (sensor.mode == mode) and (sensor.location == location):
			return sensor
	return None

def process_sensors(sensors, adafruit):
	# send all the primary values
	temperatures = {}
	for sensor in sensors:
		sensor.sample()
		if sensor.mode == "primary":
			sensor.send_to_adafruit(adafruit)
			if (sensor.location == "inside") or (sensor.location == "outside") :
				temperatures[sensor.location] = sensor.temperature

	# now send all the comparison's
	for sensor in sensors:
		if (sensor.mode == "primary") and (sensor.location == "outside"):
			other = find_sensor("compare" ,sensor.location)
			if other and adafruit:
				other.send_to_adafruit(adafruit, sensor.temperature - other.temperature)

	return temperatures

def process_powerswitch(powerswitch, temperatures, gmail):
	# now we process the powerswitch, if it exists
	if powerswitch and powerswitch.process(temperatures['inside']):
		logging.info("heater changing %s" % powerswitch.enable())
		gmail.send(	
			"changing heater to %s\n"
			"temps: inside=%0.2f  outside=%0.2f\n"
			"range: low=%0.2f high=%0.2f\n" 
			"%s" % (powerswitch.enable(), 
			temperatures['inside'], temperatures['outside'],
			powerswitch.low, powerswitch.high, powerswitch.elapsed))

if __name__ == '__main__':
	# init the logger
	init_logging()

	# read in the inifile
	parser = init_inifile()

	# init adafruit
	adafruit = init_adafruit(parser)

	# init the sensors
	sensors = init_sensors(parser)

	# init the powerswitch
	powerswitch = init_power_switch(parser)

	# init gmail
	gmail = init_gmail(parser)

	# init adafruit
	consts = init_parameters(parser)

	gmail.send("Program starting. Machine uptime %s" % utils.uptime())

	for iteration in range(consts.MAX_ITERATIONS):
		measurements = 0
		try : 
			while True:
				temperatures = process_sensors(sensors, adafruit)
				process_powerswitch(powerswitch, temperatures, gmail)

				time.sleep(consts.MEASUREMENT_INTERVAL)
				measurements += 1
		except Exception, args:
			message = "Error at iteration %d, measurements %d %r" \
						% (iteration, measurements, args)
			gmail.send(message)
			logging.exception(message)

	gmail.send("Program ended with %d iterations" % const.MAX_ITERATIONS)
