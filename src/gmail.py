#!/usr/bin/env python

import smtplib		# look in /etc/ssmtp/ssmtp.config
import os
import time
import utils
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

class GMail():
	def __init__(self, user, password, subject, enabled=False):
		self.enabled = enabled
		self.email = user
		self.password = password
		self.subject = subject
		self.server = "smtp.gmail.com"
		self.port = 587
		if enabled :
			session = smtplib.SMTP(self.server, self.port)
			session.ehlo()
			session.starttls()
			session.ehlo
			session.login(self.email, self.password)
			self.session = session

	def __str__(self):
		return "enabled:%s email:%s password:%s subject:%s server:%s port:%d"% (self.enabled, self.email, self.password, self.subject, self.server, self.port)
	
	def send(self, body):
		headers = [
			"From: " + self.email,
			"Subject: " + self.subject,
			"To: " + self.email,
			"MIME-Version: 1.0",
			"Content-Type: text/plain"]
		headers = "\r\n".join(headers)
		logging.info("%s: %s",self.email,body)
		if self.enabled:
			status = self.session.sendmail(self.email, 
				self.email, headers + "\r\n\r\n" + body)
	
if __name__ == '__main__':
	try:
		user = "hunterhousepi@gmail.com"
		password = "abcd+ABCD"
		subject = os.uname()[1] + " test"
		gm = GMail(user, password, subject, True)
		now = time.asctime(time.localtime(time.time()))
		# now =  utils.now()	
		gm.send("lets see if this gets forwarded @" + now)

	except Exception, Arguement:
		print "something went wrong: ", Arguement

