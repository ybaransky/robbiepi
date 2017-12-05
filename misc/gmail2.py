#!/usr/bin/env python

import base64
import httplib2
from email.mime.text import MIMEText
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# PAth to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes 
# for all available copes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credetials storage file
STORAGE = Storage('email.storage')

flow = flow_from_clientsecrest(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is Nonw or credentials.invalid:
	credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# build the gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

# create a message
msg = MIMEText("hello from the OAutah world")
msg['to'] = "ybaransky@gmail.com"
msg['from'] = "hunterhousepi@gmail.com"
msg['subject'] = "testing"
body = {'raw' : base64.b64encode(msg.as_string())}

try:
	msg = (gmail_service.users().messages().send(usedId="me",body=body).execute())
	print 'msg id: %s' % msg['id']
	print msg
except Exception as error:
	print 'error occured: %s' % error
