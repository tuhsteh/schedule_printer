#  List of people to be used for scheduling.
#  Note that the names can certainly be changed,
#  but the structure of this file MUST remain
#  unchanged.
#  Each list below is an array of strings.
#  Each string must be contained in quotes,
#  and string items must be comma delimited.
#  They are placed on separate lines only
#  for readability, and this is not required.
#
#  This list is constructed as a list of lists.
#  Each service will get its own list of people.
#  Then, people can choose for which service they
#  would like to serve.  Currently, there are
#  two separate lists.
#
#  thomas r. stear, 7 Dec 2009
#  updated on 12 December 2011 to reflect new deaconesses
#  for the 2012-2013 serving calendar

from datetime import datetime


roster = [
    {
        "Inessa Young":[
            datetime(2013, 7, 28),
            datetime(2013, 8, 4),
            ],
        "Carrie Ramirez":[],
        "Barney Smith":[],
        "Carrie Rivas":[],
        "Georgia Schroeder":[],
        "Carrie Thomas":[],
        "David Pittman":[]
    },
    
    {
        "Harold Pugh":[],
        "Leonard Blair":[
            datetime(2013, 6, 23),
            datetime(2013, 6, 30),
            datetime(2013, 7, 7),
            datetime(2013, 7, 14),
            datetime(2013, 7, 21),
            datetime(2013, 7, 28),
            datetime(2013, 8, 4),
            ],
        "David Morales":[],
        "Inessa Pugh":[],
        "Katherine Oliver":[],
        "Barney Stamp":[],
        "Anne Leach":[
            datetime(2013, 3, 17),
            ],
        "Fred Espinoza":[],
        "Anne Mckinney":[],
        "David Espinoza":[],
        "Leonard Schroeder":[],
        "Howard Waters":[],
   }
]

serving_list = [
        "Inessa Young",
        "Carrie Ramirez",
        "Barney Smith",
        "Carrie Rivas",
        "Georgia Schroeder",
        "Carrie Thomas",
        "David Pittman",
        "Harold Pugh",
        "Leonard Blair",
        "David Morales",
        "Inessa Pugh",
        "Katherine Oliver",
        "Barney Stamp",
        "Anne Leach",
        "Fred Espinoza",
        "Anne Mckinney",
        "David Espinoza",
        "Leonard Schroeder",
        "Howard Waters",
]
