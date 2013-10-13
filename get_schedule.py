#!/usr/bin/python

#import xml.etree.ElementTree as xml
try:
	from xml.etree import ElementTree as xml
except ImportError:
	from elementtree import ElementTree as xml
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom.data
import time
import datetime
import atexit
import sys

#==============================================================================
# local_time_offset() Function
#==============================================================================
def local_time_offset(t=None):
	"""Return offset of local zone from GMT, either at present or at time t."""
	# python2.3 localtime() can't take None
	if t is None:
		t = time.time()

	if time.localtime(t).tm_isdst and time.daylight:
		retval = -time.altzone
	else:
		retval = -time.timezone
	return retval;

#==============================================================================
# sec_to_time() Function
#==============================================================================
def sec_to_time(sec):
	if sec < 0:
		neg = True;
	else:
		neg = False;
	sec = abs(sec);
	hrs = sec / 3600
	sec -= 3600*hrs

	mins = sec / 60
	sec -= 60*mins

	strtime = "%02d:%02d" % (hrs, mins);
	if neg:
		strtime = "-" + strtime;
	return strtime;

#==============================================================================
# write_sched_file() Function
#==============================================================================
def write_sched_file(feed,feedCount,sched_start_dt,schedfilepath):
	# build a tree structure
	root = xml.Element("SCHEDULES")
	root.set("source","get_schedule.py");
	root.set("updated",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"));

	purpose = xml.SubElement(root, "purpose")
	purpose.text = "Daily schedule for OpenSprinkler"

	sched_date = xml.SubElement(root, "schedule_date")
	sched_date.text = sched_start_dt

	sched_count = xml.SubElement(root, "schedule_count")
	sched_count.text = str(feedCount)

	if feedCount > 0:
		zones = xml.SubElement(root, "zones")

		for i, an_event in enumerate(feed.entry):
			print("{0}. {1}".format(i, an_event.title.text))
			zone = xml.SubElement(zones, "zone")
			name = xml.SubElement(zone, "name")
			name.text = an_event.title.text
			for a_when in an_event.when:
				print("\t\tStart time: {0}".format(a_when.start))
				print("\t\tEnd time: {0}".format(a_when.end))
				start = xml.SubElement(zone, "start")
				start.text = a_when.start
				stop = xml.SubElement(zone, "stop")
				stop.text = a_when.end

	# wrap it in an ElementTree instance, and save as XML
	tree = xml.ElementTree(root)
	tree.write(schedfilepath)

#==============================================================================
# get_sched() Function
#==============================================================================
def get_sched(caluser,magcookie,schedfilepath):

# Calendar friendly name is: 'My Sprinklers'
	projection = 'full'
	calendar_client = gdata.calendar.client.CalendarClient()
	feed_uri = calendar_client.GetCalendarEventFeedUri(calendar=caluser, visibility=magcookie, projection=projection)
	query = gdata.calendar.client.CalendarEventQuery()

	# Set the query start and end date/times to today at 00:00 until tomorrow at 00:00 to get all schedules for today
	toff = local_time_offset();
	stroffset = sec_to_time(toff);
	startdt = datetime.datetime.now().strftime("%Y-%m-%d");
	startdtm = startdt + 'T00:00:00.000' + stroffset;
	denddtm = datetime.datetime.now() + datetime.timedelta(days=1);
	enddtm = denddtm.strftime("%Y-%m-%d");
	enddtm += 'T00:00:00.000' + stroffset;
	query.start_min = startdtm;
	query.start_max = enddtm;

	# Query google calendar for the date range
	feed = calendar_client.GetCalendarEventFeed(uri=feed_uri,query=query)
	feedCount = int(feed.total_results.text.strip())
	write_sched_file(feed,feedCount,startdt,schedfilepath)

#==============================================================================
# main() Function
#==============================================================================
def main(caluser,magcookie,schedfilepath):
	print('\nGet Schedule has started...')
	get_sched(caluser,magcookie,schedfilepath)

#==============================================================================
# progexit() Function
#==============================================================================
def progexit():
	pass

#==============================================================================
# This causes the main() function to be called, and registers an exit function call
#==============================================================================
if __name__ == "__main__":
	atexit.register(progexit)

# ======================================================
# Get the required Parameters from the command line
# 3 parameters are expected:
# caluser = Google Calendar username (see below)
# magcookie = Google Calendar Magic Cookie (see below)
# schedfilepath = relative path and file name to write schedule file to
#
# caluser
# How to get caluser field value: 
# To find your calendar's username:
# In the list of calendars on the left side of the page, find the calendar you want to interact with. You can create a new calendar for this purpose if you want to.
# Click the arrow button to the right of the calendar. Select "Calendar settings" from the drop-down menu. The Calendar Details page appears.
# Scroll down to the Calendar Address section, the Calendar ID appears here.
# The format of the Calendar ID (username) is: 00000000000000000000000000@group.calendar.google.com
#
# magcookie
# How to get Visibility (Magie Cookie) field value: 
# This code uses the Google Calendar 'Magic Cookie' to authenticate
# The simplest feed URL to use is that of the calendar's read-only, "magic cookie" private feed, because that URL doesn't require authentication. The usual procedure for determining that URL involves using a JavaScript-enabled GUI browser to get the URL manually. If you can't or don't want to use such a browser, then you can instead interact with Calendar using one of the other feed URLs, which require authentication, but which you can construct without using a browser.
# To find your calendar's "magic cookie" feed URL:
# In the list of calendars on the left side of the page, find the calendar you want to interact with. You can create a new calendar for this purpose if you want to.
# Click the arrow button to the right of the calendar. Select "Calendar settings" from the drop-down menu. The Calendar Details page appears.
# Scroll down to the Private Address section and select the XML button. The feed URL appears.
# Copy the URL. This is the URL of your calendar's read-only "magic cookie" private feed; it includes a special coded string that lets you read the private feed without having to do authentication. This is the URL you'll use to request a feed from Calendar, so you won't have to do authentication just to view the feed.
# The feed URL has the following form:
# https://www.google.com/calendar/feeds/userID/private-magicCookie/basic
# More about magic cookie here: https://developers.google.com/google-apps/calendar/v2/developers_guide_protocol#AuthMagicCookie
# 
# schedfilepath
# Example schedfilepath: /home/pi/opensprinkler/sched.xml
# ======================================================

  	nargs = len(sys.argv)
	if nargs == 4:
		caluser = sys.argv[1]
		magcookie = sys.argv[2]
		schedfilepath = sys.argv[3]
#		print("caluser: {0}\nmagcookie: {1}\nschedfilepath: {2}\n".format(caluser,magcookie,schedfilepath))
		main(caluser,magcookie,schedfilepath)
	else:
		print '\nUsage: get_schedule.py caluser magcookie schedfilepath'
		print '\nExample: get_schedule.py xxx@group.calendar.google.com private-xxx /home/pi/opensprinkler/sched.xml'
