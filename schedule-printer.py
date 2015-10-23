#!/usr/bin/env python
"""
This script takes a few items from the user,
then generates a schedule for a specific
volunteer position.

In reality, any office that needs officers each
week can be filled with this scheduler,
and any number of people and any number of services
can be specified, as long as there are people to
fill those places.

thomas r. stear, 6 Dec 2009, built and tested on
    Mac OS X 10.6.2, using Python 2.6.1.

"""

import sys, os
from datetime import datetime, date, timedelta
from math import floor
from random import random

first_service = []
second_service = []

"""
This method will determine when the next Sunday is
going to be as a datetime object, which can be easily
printed as a string in your preferred format.

This takes as input a given date, and then determines
the following Sunday from that.
"""
def getNextSunday(currentDate):
    start=currentDate
    if start.weekday() == 6:
        start = start + timedelta(days=1)
    next = start + timedelta(days=(6-start.weekday()))
    return next


"""
This method will return a list of MAX people chosen roughly
at random from the globally available list of people.

The way it works is a random select with decay.  After a
random person is chosen from the top third of the list,
that person is moved to the bottom of the list, so they will not
be chosen again for a while.  This way, the schedule will
be made in a roughly random order, but people should still be
picked to serve the same number of times, and they will
get to serve with different people.

On a finer level, i simply re-add the person to the bottom of
the original list, then delete the specific row i was using in
the first place.  That way, the person is not missing from the
list, and i don't have to bubble up people to fill in a hole.

"""
def build_list(MAX, list_choice = 'first_service'):
    list = first_service if list_choice == 'first_service' else second_service

    window = int(floor(len(list)/3))
    temp = []
    for n in range (0, MAX):
        i = int(floor(window*random()))
        temp.append(list[i])
        list.append(list[i])
        del list[i]
    return temp


"""
Currently set to report in HTML format.  This method 
prints the leading information required for the HTML
document to be interpreted properly.

"""
def printHead(FILE, personnel):
    try:
        FILE.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<HTML>\n<HEAD>\n<TITLE>%s Schedule for Next Year</TITLE>\n</HEAD>\n<BODY>\n" % personnel)
    except Exception as e:
        print "There was an error writing the file head:  %s" % e


"""
Currently set to report in HTML format.  This method 
prints the tailing information required for the HTML
document to be interpreted properly.

"""
def printTail(FILE):
    try:
        FILE.write("\n</BODY>\n</HTML>")
    except Exception as e:
        print "There was an error writing the file tail:  %s." % e


"""
This method implements the template for printing the 
schedule.  Currently prints in a two column format, 
writing each day's schedule left to right, then down.

"""
def printTable(FILE, sunday, list):
    try:
        FILE.write('\n<TABLE BORDER=0>\n')
        FILE.write('<TR><STRONG>%s</STRONG></TR>\n' % sunday.strftime("%d %B %Y"))
        svc = 1
        for svc_sched in list:
            svcStr = "1st" if svc==1 else ("2nd" if svc==2 else "3rd")
            FILE.write('<TR><TD><EM>%s</EM></TD>' % svcStr)
            FILE.write('<TD>%s</TD></TR>\n' % '<BR>\n'.join(svc_sched))
            svc = svc + 1
        FILE.write('</TABLE>\n')
    except Exception as e:
        print "There was an error writing a table to the file:  %s" % e


"""
The bigger, outer part of the pretty printer.  This takes the whole
dictionary, and writes out tables for each sunday, each service,
each group of people for each service, ....

"""
def printSched(FILE, sched, dates):
    import ipdb
    ipdb.set_trace()
    try:
        FILE.write('<TABLE BORDER = 1>')
        for i in range (0, len(dates)/4+1):
            FILE.write('<TR><TD>')
            printTable(FILE, dates[i*4], sched[i*4])
            FILE.write('</TD><TD>')
            if i*4+1 < len(dates):
                printTable(FILE, dates[i*4 + 1], sched[i*4 + 1])
                FILE.write('</TD><TD>')
            if i*4+2 < len(dates):
                printTable(FILE, dates[i*4 + 2], sched[i*4 + 2])
                FILE.write('</TD><TD>')
            if i*4+3 < len(dates):
                printTable(FILE, dates[i*4 + 3], sched[i*4 + 3])
                FILE.write('</TD></TR>\n')
        FILE.write('</TABLE>\n')
    except Exception as e:
        print "There was a problem reporting the schedule:  %s." % e


"""
Simple set of steps:
  1.  Get a list of people from the user.
  2.  Ask the user how many services, and how many people for each service.
  3.  Build a list of people for each service and write it to the file.
  4.  Profit.

NOTE:  The list of people to feed in must be contained in a file
  called 'roster.py' in the same folder as this script.  The script is
  NOT smart enough to go looking for it, and i will NOT be adding
  that feature ever.

"""
if __name__ == "__main__":
    from roster import list
    first_service = list[0]
    second_service = list[1]

    try:
        FILE = open("report.html", 'w')
    except Exception as e:
        print "There was a problem opening the output file:  %s." % e
        exit(2)
    
    if len(first_service) < 1:
        print "There was a problem loading the first roster.  It appears to have no people in it.  Please check the file path, filename, file location, variables list, and read the directions and try again."
        exit(1)
    if len(second_service) < 1:
        print "There was a problem loading the second roster.  It appears to have no people in it.  Please check the file path, filename, file location, variables list, and read the directions and try again."
        exit(1)
    sched_type = raw_input("What type of schedule are we making today (e.g. Elders, Deacons, Accolytes, ...)?  ")
    svc_count  = raw_input("How many services are there every Sunday for which you are scheduling %s?  " % sched_type)
    svc_req = []
    try:
        svc_count = int(svc_count)
    except Exception as e:
        print "There was a problem with the number you entered:  %s." % e
        exit(3)
    for i in range (0, svc_count):
        resp = raw_input("How many %s are required for service %d?  " % (sched_type, i+1))
        try:
            resp = int(resp)
        except Exception as e:
            print "There was a problem with the number you entered:  %s." % e
            exit(3)

        svc_req.append(resp)
    
    sched = []
    dates = []
    sunday = datetime(2011, 2, 7)
    for i in range (0,52):
        sunday = getNextSunday(sunday)
        dates.append(sunday)

        svc_ppl = []
        for j in range(0,svc_count):
            if j == 0:
                list_choice = 'first_service'
            elif j == 1:
                list_choice = 'second_service'
            f = build_list(svc_req[j], list_choice)
            svc_ppl.append(f)
        sched.append(svc_ppl)
        
    printHead(FILE, sched_type)
    printSched(FILE, sched, dates)
    printTail(FILE)

    try:
        FILE.close
    except Exception as e:
        print "There was an error closing the file.  Your work may be lost.  %s." % e




