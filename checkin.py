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
	checkinUrl = urlparse.urljoin(baseUrl, '/flight/retrieveCheckinDoc.html')
	retrieveUrl = urlparse.urljoin(baseUrl, infoUrl)

	req = urllib2.Request(url=retrieveUrl)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	resp = opener.open(req)
	swData = resp.read()

	soup = BeautifulSoup(swData, "html.parser")
	flights = []
	for flight in soup.find_all("tr"):
		day = None
		for date in flight.find_all("span", { "class" : "itinerary-table--summary-travel-date"}):
			day = timeModule.strptime(date.string, '%A, %B %d, %Y')
		if day == None:
			continue
		print day
		#for time in flight.find_all("span", { "class" : "nowrap" })[::2]:
		#	print time.string
		#for depart in flight.find_all("div", {"class" : "itinerary-table--segment-flight-stops routingDetailsStops"})[::2]:
		#	print depart.string