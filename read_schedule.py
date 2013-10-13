#!/usr/bin/python

try:
	from xml.etree import ElementTree as xml
except ImportError:
	from elementtree import ElementTree as xml
import time
import datetime
import atexit
import sys
import subprocess

#==============================================================================
# read_sched_file() Function
#==============================================================================
def read_sched_file(schedfile,cronfile):
	tree = xml.parse(schedfile)
	elem = tree.getroot()
	sched_date = elem.find("schedule_date")
	if sched_date is None:
		# Handle no section called schedule_date found in xml file
		print "arghh 1!!!!"
	else:
		scheddt = sched_date.text
		todaydt = datetime.datetime.now().strftime("%Y-%m-%d");
		if scheddt.strip() != todaydt.strip():
			# Handle date mismatch in xml file
			print "arghh 2!!!!"
		else:
			sched_count = elem.find("schedule_count")
			if sched_count is None:
				# Handle no section called schedule_count found in xml file
				print "arghh 3!!!!"
			else:
				count = sched_count.text
				if int(count) > 0:
					zones = elem.find('zones')
					if zones is None:
						# Handle no section called zones found in xml file
						print "arghh 4!!!!"
					else:
						if len(zones.findall('zone')) == 0:
							print "argh 5!!!!"
							# Handle no section called zone found in xml file
						else:
							f = open(cronfile, 'w')
							for zone in zones.findall('zone'):
								zonename = zone.find("name")
								start = zone.find("start")
								stop = zone.find("stop")
								print '\t%s' % (zonename.text)
								print '\t%s' % (start.text)
								print '\t%s' % (stop.text)
								print todaydt
								sttimeonly = start.text[11:16]
								print sttimeonly
								#call function to schedule chron jobs here
								f = open('datetime.sh','w')
								f.write('#!/bin/bash\n')
								f.write('echo "It is now $(date +%T) on $(date +%A)"\n')
								f.write('echo "This batch script was written by the python app"\n')
								f.close()
								p = subprocess.Popen(["at", "-f", "datetime.sh", sttimeonly, todaydt], stdout=subprocess.PIPE)
								out, err = p.communicate()
								if p.returncode != 0:
									raise OSError('at error')
							print "stdout is: "
							print out
							print "sterr is: "
							print err

#==============================================================================
# main() Function
#==============================================================================
def main(schedfilepath):
	print('Read_schedule has started...')
	read_sched_file(schedfilepath,"cronadd.txt")

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
  
   	nargs = len(sys.argv)
  	if nargs == 2:
  		schedfilepath = sys.argv[1]
  		print("\nschedfilepath: {0}\n".format(schedfilepath))
  		main(schedfilepath)
  	else:
  		print '\nUsage: read_schedule.py schedfilepath'
  		print '\nExample: read_schedule.py /home/pi/opensprinkler/sched.xml'
