# Roman Numerals
# 2010-06-15, Eljakim Schrijvers

mapping = [ ('cd',4*'c'),
            ('xl',4*'x'),
            ('iv',4*'i'),
            ('d',5*'c'),
            ('l',5*'x'),
            ('v',5*'i'),
            ('cm',9*'c'),
            ('xc',9*'x'),
            ('ix',9*'i')]

bignums = [ ('m',1000), ('c',100), ('x', 10), ('i',1) ]

## vegaseat function for error check
def int2roman(number):
    numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL", 
        50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D", 900 : "CM", 1000 : "M" }
    result = ""
    for value, numeral in sorted(numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result

def fromroman(x):
    for (shortv, longv) in mapping: x= x.replace(shortv, longv) ## reverse order needed
    x = '+'.join(list(x))
    for (character, word) in bignums: x = x.replace(character, str(word))
    if x=='': x = '0'
    return eval(x)

def toroman(x):
    val = ''
    for (character, word) in bignums:
        val = val + (x / word) * character
        x = x % word
    for (shortv, longv) in reversed(mapping): ## reverse here not permanantly
        val = val.replace(longv,shortv)
    return val

'''
bugs1 = bugs2 = 0
for i in range(5000):
    if fromroman(toroman(i)) != i:
        print ('Reverse failure: %i, %s, %s' % (i,toroman(i),fromroman(toroman(i))))
        bugs1+=1

    if  int2roman(i).lower() != toroman(i): 
        print ('Wrong roman: %i, %s, %s' % (i,int2roman(i),toroman(i)))
        bugs2+=1

'''

""" Last ilne of output:
Test passed!
"""