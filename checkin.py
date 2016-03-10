import re, sys, sched, datetime, urllib, urllib2, urlparse
import time as timeModule
from datetime import datetime,date,timedelta,time
from pytz import timezone,utc
from bs4 import BeautifulSoup, Tag
from mechanize import Browser

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
	day = None

	soup = BeautifulSoup(swData, "html.parser")
	for flight in soup.find_all("tr"):
		for date in flight.find_all("span", { "class" : "itinerary-table--summary-travel-date"}):
			for time in flight.find_all("span", { "class" : "nowrap" })[::2]:
				day = datetime.fromtimestamp(timeModule.mktime(timeModule.strptime(date.string+' '+time.string, '%A, %B %d, %Y %I:%M %p')))
		if day == None:
			continue
		day = day - timedelta(days=1)
		if day.date() == datetime.today().date():
			break

	if day == None:
		print 'No flight found. Make sure information is correct.'
		quit()
	if day.date() != datetime.today().date() or day.date() == (day +timedelta(days=1)):
		print 'No flight found for tomorrow. Make sure information is correct.'
		quit()

	print 'Checking in on ' + day.strftime('%B %d') + ' at ' + day.strftime('%I:%M %p')
	waitTime = day - datetime.today()

	if (waitTime.total_seconds()>0):
		print 'Waiting to check in for '+  str(waitTime)
		timeModule.sleep(waitTime.total_seconds()-1)

	br = Browser()
	loop = True
 	while loop:
		br.open(checkinUrl)
		for form in br.forms():
			print form.name
			if form.name == "checkinOptions":
				loop = False
				break

	br.select_form(name="checkinOptions")
	req = br.submit(name="printDocuments")
	soup = BeautifulSoup(br.response().read(), "html.parser")
	position = soup.find_all('span', {"class" :"boardingInfo"})
	print 'Boarding Position: ' + position[0].string + position[1].string
	