import datetime
import calendar
import re
from cch.fuzzydate.core import FuzzyDate

# regression test for FuzzyDate
# run it without parameters
# it will call setAsString and getAsString for a series of dates
# for any of those dates, if it prints "EXPECTED" then the conversion failed

dates = [
         # date ranges
         ['2009/01/01 to 2009/02/01', '2009-01-01 to 2009-02-01'],
         ['2009/02/01 - 2009/03/01', '2009-02-01 to 2009-03-01'],
         ['2009/03/02 2009/03/20', '2009-03-02 to 2009-03-20'],
         ['2009/01/01, 2009/02/01', '2009-01-01 to 2009-02-01'],
         ['2009/01, 2009/02', '2009-01 to 2009-02'],
         ['2009 - 2010', '2009 to 2010'],
         ['?2009 - 2010', '?2009 to 2010'],
         ['? 2009 to 2010', '?2009 to 2010'],
         ['? 2009/02 - 2009/04', '?2009/02 to 2009/04'],
         # single dates
         ['24-12-2009', '24-12-2009'],
         ['2009-01-01', '2009-01-01'],
         ['2009/01', '2009-01'],
         ['2009', '2009'],
         ['c. 2009', 'c. 2009'],
         ['c.2009', 'c. 2009'],
         ['? 2009', '?2009'],
         ['?2009', '?2009'],
         # wrong formats (E means an error is raised)
         ['err 2009', 'E'],
         ['2009-sdfa', 'E'],
         ['2009-01-01-01', 'E'],
         ['2009-02-34', 'E'],
         ['24-12-2009', 'E'],
         # year is less than 1000
         ['2009', '456'],
         [None, ''],
         ]

# UK Format
dates = {
         # date ranges
         '01/01/2009 to 01/02/2009': '1-1-2009 to 1-2-2009',
         '01/02/2009 - 01/03/2009': '1-2-2009 to 1-3-2009',
         '02/03/2009 20/03/2009': '2-3-2009 to 20-3-2009',
         '01/01/2009, 01/02/2009': '1-1-2009 to 1-2-2009',
         '01/2009, 02/2009': '1-2009 to 2-2009',
         '2009 - 2010': '2009 to 2010',
         '?2009 - 2010': '?2009 to 2010',
         '? 1/2009 to 3/2009': '?1-2009 to 3-2009',
         '? 2009, 2010': '?2009 to 2010',
         # single dates
         '24-12-2009': '24-12-2009',
         '1-1-2009': '1-1-2009',
         '3-11-2009': '3-11-2009',
         '01-01-2009': '1-1-2009',
         '01/2009': '1-2009',
         '2009': '2009',
         'c. 2009': 'c. 2009',
         'c.2009': 'c. 2009',
         '? 2009': '?2009',
         '?2009': '?2009',
         # wrong formats (E means an error is raised)
         'err 2009': 'E',
         '2009-sdfa': 'E',
         '01-01-01-2009': 'E',
         '34-02-2009': 'E',
         '2009-12-24': 'E',
         # year is less than 1000
         '105': '105',
         '10-01-010': '10-1-10',
         'c. 1': 'c. 1',
         None : ''
         }

error_count = 0
test_id = 0
    
d = FuzzyDate()
for datestr, expected in dates.iteritems():
    test_id += 1
    print "#%d - Set '%s'" % (test_id, datestr)
    res = d.setAsString(datestr)
    converted = d.getAsString()
    print "\tINTERNAL : '%s'" % d.__repr__()
    print "\tCONVERTED: '%s'" % converted
    if (not res):
        print "\tERROR    : %s" % d.getLastError()
        converted = 'E'
    if (len(expected) > 0 and converted != expected):
        print "\tEXPECTED : '%s' !" % expected
        error_count += 1
    print ""

print "%d errors." % error_count
