import re, sys, sched, datetime, urllib, urllib2, urlparse
import time as timeModule
from datetime import datetime,date,timedelta,time
from pytz import timezone,utc
from bs4 import BeautifulSoup
from bs4 import Tag

if __name__ == '__main__':
	firstName = raw_input("First Name: ")
	lastName = raw_input("Last Name: ")
	confirmation = raw_input("Confirmation Number: ")

	baseUrl = 'https://www.southwest.com'
	infoUrl = '/flight/view-air-reservation.html?confirmationNumberFirstName='+firstName+'&confirmationNumberLastName='+lastName+'&confirmationNumber='+confirmation
	retrieveUrl = urlparse.urljoin(baseUrl, infoUrl)
	dataUrl = '/flight/retrieveCheckinDoc.html?firstName='+firstName+'&lastName='+lastName+'&confirmationNumber='+confirmation
	checkinUrl = urlparse.urljoin(baseUrl, dataUrl)

	req = urllib2.Request(url=retrieveUrl)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	resp = opener.open(req)
	swData = resp.read()

	soup = BeautifulSoup(swData, "html.parser")
	for flight in soup.find_all("tr"):
		day = None
		for date in flight.find_all("span", { "class" : "itinerary-table--summary-travel-date"}):
			# TODO timezone flight.find_all("div", {"class" : "itinerary-table--segment-flight-stops routingDetailsStops"})[::2]:
			for time in flight.find_all("span", { "class" : "nowrap" })[::2]:
				day = datetime.fromtimestamp(timeModule.mktime(timeModule.strptime(date.string+' '+time.string, '%A, %B %d, %Y %I:%M %p')))
		if day == None:
			continue
		day = day - timedelta(days=1)
		#if day.date() == datetime.today().date(): TODO
		break

	print 'Checking in on ' + day.strftime('%B %d') + ' at ' + day.strftime('%I:%M %p')
	waitTime = day - datetime.today()

	#if (waitTime.total_seconds()>10):
	#	print 'Waiting for '+  str(waitTime)
	#	timeModule.sleep(waitTime.total_seconds())
	#waitTime = day - datetime.today()
	#print 'Waiting for '+  str(waitTime)
	#timeModule.sleep(waitTime.total_seconds())
	# TODO: add back, does sleep work well

	req = urllib2.Request(url=checkinUrl)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	resp = opener.open(req)
	swData = resp.read()
	print swData #TODO remove

	soup = BeautifulSoup(swData, "html.parser")
	# TODO keep going




	