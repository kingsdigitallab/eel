from enum import Enum

e = Enum()
e.addElement('MONDAY', {'symbol': 'mo'})
e.addElement('TUESDAY', {'symbol': 'tu'})
d = e.MONDAY
print d.symbol
d = e.getElement(1)
print d.id

exit()
