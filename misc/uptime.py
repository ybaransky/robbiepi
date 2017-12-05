#!/usr/bin/env python

from datetime import timedelta

with open('/proc/uptime','r') as f:
	uptime_seconds = round(float(f.readline().split()[0]))
	uptime_string = str(timedelta(seconds = uptime_seconds))

print uptime_seconds, uptime_string
