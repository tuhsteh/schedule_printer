
import sys, os
from datetime import datetime, date, timedelta
from math import floor
from random import random as r
from Person import Person



class Scheduler:
    reportFileName = "report.html"
    a = []
    b = []
    startingDate = datetime(2013, 2, 16)
    
    def __init__(self):
        pass
    
    def getNextSunday(self, currentDate):
        start=currentDate
        start = start + timedelta(days=1) if start.weekday() == 6 else start
        next = start + timedelta(days=(6-start.weekday()))
        return next
        
        
    def buildSingleDay(self, currentDate, MAX, list_choice = 'a'):
        people = self.a if list_choice == 'a' else self.b
        window = int(floor(len(people)/3))
        temp = []
        for n in range (0, MAX):
            i = int(floor(window*r()))
            while (not people[i].isAvailable(currentDate)):
                i += 1
            temp.append(people[i].name)
            people.append(people[i])
            del people[i]
        return temp
    
    
    def printHead(self, FILE, personnel_type):
        try:
            FILE.write( self.FILE_HEADER % personnel_type)
        except Exception as e:
            print "There was an error writing the file head:  %s" % e
    
    
    def printTail(self, FILE):
        try:
            FILE.write("\n</BODY>\n</HTML>")
        except Exception as e:
            print "There was an error writing the file tail:  %s." % e


    def printTable(self, FILE, sunday, list):
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


    def printSched(self, FILE, sched, dates):
        try:
            FILE.write('<TABLE BORDER = 1>')
            for i in range (0, len(dates)/4+1):
                FILE.write('<TR><TD>')
                self.printTable(FILE, dates[i*4], sched[i*4])
                FILE.write('</TD><TD>')
                if i*4+1 < len(dates):
                    self.printTable(FILE, dates[i*4 + 1], sched[i*4 + 1])
                    FILE.write('</TD><TD>')
                if i*4+2 < len(dates):
                    self.printTable(FILE, dates[i*4 + 2], sched[i*4 + 2])
                    FILE.write('</TD><TD>')
                if i*4+3 < len(dates):
                    self.printTable(FILE, dates[i*4 + 3], sched[i*4 + 3])
                    FILE.write('</TD></TR>\n')
        except IndexError as ie:
            pass
        except Exception as e:
            print "There was a problem reporting the schedule:  %s." % e
        finally:
            FILE.write('</TABLE>\n')


    def getPeople(self, list):
        return [Person(name, restrictions) for name, restrictions in list.iteritems()]
        
    
    def finalReport(self):
        from roster import serving_list as s
        try:
            f = open(self.reportFileName, 'r')
            r = f.read()
            for i in s:
                print "%d:\t%s" % (r.count(i),i)
            f.close()
        except:
            print "File error."
            

    def main(self):
        from roster import roster
        self.a = self.getPeople(roster[0])
        self.b = self.getPeople(roster[1])

        try:
            FILE = open(self.reportFileName, 'w')
        except Exception as e:
            print self.ERROR_OPENING_FILE % e
            exit(2)
    
        if len(self.a) < 1:
            print self.PROBLEM_ROSTER
            exit(1)
        if len(self.b) < 1:
            print self.PROBLEM_ROSTER
            exit(1)
        sched_type = raw_input( self.WHAT_KIND_OF_SCHED )
        svc_count  = raw_input( self.HOW_MANY_SERVICES % sched_type)
        svc_req = []
        try:
            svc_count = int(svc_count)
        except Exception as e:
            print self.ERROR_NUMBER_ENTRY % e
            exit(3)
        for i in range (0, svc_count):
            resp = raw_input( self.HOW_MANY_SERVERS % (sched_type, i+1))
            try:
                resp = int(resp)
            except Exception as e:
                print self.ERROR_NUMBER_ENTRY % e
                exit(3)

            svc_req.append(resp)
    
        sched = []
        dates = []
        sunday = self.startingDate
        for i in xrange (0,53):
            sunday = self.getNextSunday(sunday)
            dates.append(sunday)

            svc_ppl = []
            for j in range(0,svc_count):
                list_choice = 'a' if j == 0 else 'b'
                f = self.buildSingleDay(sunday, svc_req[j], list_choice)
                svc_ppl.append(f)
            sched.append(svc_ppl)
        
        self.printHead(FILE, sched_type)
        self.printSched(FILE, sched, dates)
        self.printTail(FILE)

        try:
            FILE.close
        except Exception as e:
            print self.ERROR_CLOSING_FILE % e
        print "Your schedule is all set!  See report.html"
        self.finalReport()


    FILE_HEADER        = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<HTML>\n<HEAD>\n<TITLE>%s Schedule for Next Year</TITLE>\n</HEAD>\n<BODY>\n" 
    ERROR_OPENING_FILE = "There was a problem opening the output file:  %s."
    ERROR_CLOSING_FILE = "There was an error closing the file.  Your work may be lost.  %s."
    ERROR_NUMBER_ENTRY = "There was a problem with the number you entered:  %s."
    HOW_MANY_SERVICES  = "How many services are there every Sunday for which you are scheduling %s?  "
    HOW_MANY_SERVERS   = "How many %s are required for service %d?  "
    WHAT_KIND_OF_SCHED = "What type of schedule are we making today (e.g. Elders, Deacons, Accolytes, ...)?  "
    PROBLEM_ROSTER     = "There was a problem loading this roster.  It appears to have no people in it.  Please check the file path, filename, file location, variables list, and read the directions and try again."



if __name__ == "__main__":
    s = Scheduler()
    s.main()
    