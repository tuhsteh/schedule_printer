#!/usr/bin/env python
"""
This script takes a few items from the user,
then generate a schedule for deacons/elders/....

In reality, any office that needs officers on
Sunday morning can be filled with this scheduler,
and any number of people and any number of services
can be specified, as long as there are people to
fill those places.

Feature creep, here we come.

thomas r. stear, 6 Dec 2009, built and tested on
    Mac OS X 10.6.2, using Python 2.6.1.

"""


import sys, os
from datetime import datetime, date, timedelta
from math import floor
from random import random


a = []
b = []

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

The way it works is a random select with decay, sort of.  After
a random person is chosen from the top third of the list about,
that person is moved to the bottom of the list, so they will not
be chosen again for a while.  In this way, the schedule will
be made in a roughly random order, but people should still be
picked to serve the same number of times about, and they will
get to serve with different people everytime.

On a finer level, this is mostly handled by Python's list
management, which i love.  To randomly choose someone, them move
their name to the bottom of the list would be an otherwise
difficult computation, but in Python, i can simply re-add the
person to the bottom of the original list, then delete the specific
row i was using in the first place.  That way, the person is
not missing from the list, and i don't have to bubble up
people to fill in a hole.

The reason the list is used in a global sense is that makes it
so a person will be chosen at random.  Otherwise, the bottom two
thirds of the list would never serve. 
"""
def build_list(MAX, list_choice = 'a'):
    if list_choice == 'a':
        list = a
    elif list_choice == 'b':
        list = b

    window = int(floor(len(list)/3))
    temp = []
    for n in range (0, MAX):
        i = int(floor(window*random()))
        temp.append(list[i])
        list.append(list[i])
        del list[i]
    return temp


"""
When more advanced reporting is added, this method is
here just as a placeholder to add any header information
required for various file formats (e.g. HTML).

"""
def printHead(FILE, personnel):
    try:
        FILE.write("Schedule for Next Year for %s.\n" % personnel)
    except Exception as e:
        print "There was an error writing the file head:  %s" % e


"""
When more advanced reporting is added, this method is 
here just as a placeholder to add any final or closing
statements that might be required for various file formats
(e.g. HTML).

"""
def printTail(FILE):
    try:
        FILE.write("End of schedule.")
    except Exception as e:
        print "There was an error writing the file tail:  %s." % e


"""
This method is also a placeholder, but is here implemented
for plaintext output.  This way there is a simple, pretty way
to write out the list of people chosen for a particular service.

"""
def printTable(FILE, sunday, list):
    try:
        FILE.write('------------------------------\n')
        FILE.write(sunday.strftime("%d %B %Y"))
        FILE.write('\n------------------------------\n')
        svc = 1
        for svc_sched in list:
            svcStr = "first" if svc==1 else ("second" if svc==2 else "third")
            FILE.write('    People chosen for %s service.\n' % svcStr)
            FILE.write('%s\n' % '\n'.join(svc_sched))
            svc = svc + 1
        FILE.write('------------------------------\n\n\n')
    except Exception as e:
        print "There was an error writing a table to the file:  %s" % e


"""
The bigger, outer part of the pretty printer.  This takes the whole
dictionary, and writes out tables for each sunday, each service,
each group of people for each service, ....

"""
def printSched(FILE, sched, dates):
    for list, sunday in zip(sched, dates):
        printTable(FILE, sunday, list)







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
    a = list[0]
    b = list[1]

    try:
        FILE = open("report.txt", 'w')
    except Exception as e:
        print "There was a problem opening the output file:  %s." % e
        exit(2)
    
    if len(a) < 1:
        print "There was a problem loading the first roster.  It appears to have no people in it.  Please check the file path, filename, file location, variables list, and read the directions and try again."
        exit(1)
    if len(b) < 1:
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
    sunday = datetime(2011, 1, 3)
    for i in range (0,53):
        sunday = getNextSunday(sunday)
        dates.append(sunday)

        svc_ppl = []
        for j in range(0,svc_count):
            if j == 0:
                list_choice = 'a'
            elif j == 1:
                list_choice = 'b'
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




