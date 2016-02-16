import re
import sys
import time as time_module
import sched
import datetime
import urllib
import urllib2
import urlparse
from datetime import datetime,date,timedelta,time
from pytz import timezone,utc
from bs4 import BeautifulSoup
from bs4 import Tag

class HtmlFormParser(object):
    def __init__(self, tag):
    	self.type = tag.get('type', 'text')
      	self.name = tag.get('name', '')
      	self.value = tag.get('value', '')

if __name__ == '__main__':
	firstName = raw_input("First Name: ")
	lastName = raw_input("Last Name: ")
	confirmation = raw_input("Confirmation Number: ")

	baseUrl = 'https://www.southwest.com'
	checkinUrl = urlparse.urljoin(baseUrl, '/flight/retrieveCheckinDoc.html')
	retrieveUrl = urlparse.urljoin(baseUrl, '/flight/view-air-reservation.html')

	headers = {}
	headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1'
	req = urllib2.Request(url=retrieveUrl, headers=headers)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	resp = opener.open(req)
	swData = resp.read()
	formUrl = resp.geturl()

	soup = BeautifulSoup(swData, "html.parser")
	form = soup.find('form', id='pnrFriendlyLookup_check_form')
	formaction = form.get('action', None)
	submitUrl = urlparse.urljoin(formUrl, formaction)
	inputs = []
	for i in form.findAll('input'):
		input = HtmlFormParser(i)
		if input.type == 'text' and input.name == 'confirmationNumberFirstName':
       			input.value = firstName
			inputs.append(input)
		if input.type == 'text' and input.name == 'confirmationNumberLastName':
        		input.value = lastName
			inputs.append(input)
		if input.type == 'text' and input.name == 'confirmationNumber':
        		input.value = confirmation
			inputs.append(input)
	params = []
	for i in inputs:
		params.append((i.name, i.value))

	str_params = urllib.urlencode(params, True)
	print submitUrl
	print str_params
	req = urllib2.Request(url=submitUrl, data=str_params, headers=headers)
	resp = opener.open(req)
	print resp.geturl()
	reservations = resp.read()
