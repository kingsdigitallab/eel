#  strnatcmp.py -- Perform 'natural order' comparisons of strings in python
#  Copyright (C) 2003 by Caolan McNamara <caolan@skynet.ie>
#
#  strnatcmp.py is an *altered* version of strnatcmp.c simply modified from C
#  to python.
#
#  strnatcmp.c -- Perform 'natural order' comparisons of strings in C.
#  Copyright (C) 2000 by Martin Pool <mbp@humbug.org.au>
#
#  This software is provided 'as-is', without any express or implied
#  warranty.  In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.
#

# GN: accessed 15/11/10
# http://www.csn.ul.ie/~caolan/Packages/python-natsort.html
# http://sourcefrog.net/projects/natsort/
# http://www.csn.ul.ie/~caolan/pub/python-natsort/python-natsort-1.0.0.tar.gz
#

##import curses.ascii
import ascii
from string import upper

def _isspace(a):
	if len(a):
		return ascii.isspace(a)
	return 0

def _isdigit(a):
	if len(a):
		return ascii.isdigit(a)
	return 0

def _compare_right(a, b):
	ai = 0
	bias = 0
		
#	The longest run of digits wins.  That aside, the greatest
#	value wins, but we can't know that it will until we've scanned
#	both numbers to know that they have the same magnitude, so we
#	remember it in BIAS.
	while(1):
		if (not _isdigit(a[ai:ai+1]) and not _isdigit(b[ai:ai+1])):
			return bias
		elif (not _isdigit(a[ai:ai+1])):
			return -1;
		elif (not _isdigit(b[ai:ai+1])):
			return +1
		elif (a[ai:ai+1] < b[ai:ai+1]):
			if (bias == 0):
				bias = -1;
		elif (a[ai:ai+1] > b[ai:ai+1]):
			if (bias == 0):
				bias = +1;
		elif (not a[ai:ai+1] and not b[ai:ai+1]):
			return bias;
		ai = ai + 1
	return 0

def _compare_left(a, b):
	ai = 0
#	Compare two left-aligned numbers: the first to have a
#	different value wins.
	while (1):
		if (not _isdigit(a[ai:ai+1]) and not _isdigit(b[ai:ai+1])):
			return 0;
		elif (not _isdigit(a[ai:ai+1])):
			return -1;
		elif (not _isdigit(b[ai:ai+1])):
			return +1;
		elif (a[ai:ai+1] < b[ai:ai+1]):
			return -1;
		elif (a[ai:ai+1] > b[ai:ai+1]):
			return +1;
		ai = ai + 1
	return 0

def _strnatcmp0(a, b, fold_case):
	ai = bi = 0;
	while (1):
		ca = a[ai:ai+1]
		cb = b[bi:bi+1]

# 		skip over leading spaces or zeros
	  	while (_isspace(ca)):
	       		ai = ai + 1;
	       		ca = a[ai:ai+1];

		while (_isspace(cb)):
			bi = bi + 1;
			cb = b[bi:bi+1];

# 		process run of digits
		if (_isdigit(ca) and  _isdigit(cb)):
			fractional = (ca == '0' or cb == '0')

			if (fractional):
				result = _compare_left(a[ai:], b[bi:])
				if (result != 0):
					return result;
			else:
				result = _compare_right(a[ai:], b[bi:])
				if (result != 0):
					return result;

		if (not ca and not cb):
#			The strings compare the same.  Perhaps the caller
#			will want to call strcmp to break the tie.
			return 0

		if (fold_case):
			ca = upper(ca)
			cb = upper(cb)
	  
		if (ca < cb):
			return -1;
		elif (ca > cb):
			return +1;

		ai = ai + 1
		bi = bi + 1;

def strnatcmp(a, b):
     return _strnatcmp0(a, b, 0);

# Compare, recognizing numeric string and ignoring case.
def strnatcasecmp(a, b):
     return _strnatcmp0(a, b, 1);

if __name__ == '__main__':
	items = [ '11test', '9test', '10test', 'foobar10', 'Foobar0', 'foobar' ]

	items.sort(strnatcmp)

	print 'case matters....'
	for item in items:
		print item 

	print ''

	items.sort(strnatcasecmp)

	print 'case doesn\'t matter....'
	for item in items:
		print item 
