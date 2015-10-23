# schedule_printer
Console app for scheduling a group of volunteers to serve on a weekly basis.

## Why??
My spouse's church had a scheduling problem every year.  After selecting volunteers, each committee needed 
to plan dates for those volunteers to serve.  It would be simple enough to just cycle through the group of 
volunteers, taking however many were needed from the list, and planning it for the year that way.  

But I thought it could be more refreshing to have volunteers work with different people each week.  So I 
devised this schedule printer to take the list of volunteers, and choose the needed number of people from
the list randomly.  New faces working together!

## Random Selection With Decay
My algorithm is simple:  Randomly choose the number of volunteers from the top 3rd of the list, move those selected
to the end of the list, then move on to the next week.
Let's say there are 18 volunteers, and 4 are needed each week.  
1.  From the top 6, choose 4 at random.
2.  Move those 4 to the end of the list, leaving the other 2 from what was the top 3rd, and advancing 4 other people.
3.  Again choose 4 more people.  Chance is about even that those 2 who dodged the last pick will get picked up this time.
4.  Keep going.

At the end, a report file is written, grouping the selected volunteers, and setting it all in a table like a calendar.

## Version 1
The first attempt allowed for scheduling multiple service times, and had either HTML or TXT output, like the HTML shown:

![Report Sample](https://raw.githubusercontent.com/tuhsteh/schedule_printer/version1/report_sample_v1.png "Version 1 report sample")

In practice, it usually worked pretty well at evenly distributing services to each volunteer, so they all served nearly the same number of times.

## Version 2
The first version did not easily allow for people to request a time off, if they knew they had a camping trip planned that summer for instance.  So in Version 2, I created a Class to store a Person's name and a list of Blackout dates.  The roster was not a list of people any more, it was a dictionary pairing a name with a list of dates.  

Also, the console app would print out the counts for each person, to quickly show how many times each person was scheduled to serve.  

I also upgraded the styling in the report to make it easier to read.  

![Report Sample](https://raw.githubusercontent.com/tuhsteh/schedule_printer/version2/report_sample_v2.png "Version 2 report sample")

In practice, someone with blackout dates seemed to get picked just as often as other people with no blackout dates.  Even the summer camp director, who had 9 weeks off in a row, still was only off by 1 service time compared to other people.  

## Try it yourself!
To run this app, clone the repo somewhere, and then simply execute it with Python.
```|bash
$ python sched_html_report.py
```
for version 1, or 
```|bash
$ python Scheduler.py 
```
for version 2.

It's built for python 2, and seems to run fine with python 2.6 - 2.7.  No third-party libraries are needed.  
