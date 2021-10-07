from django.core.management.base import BaseCommand
from optparse import make_option
from eel.editions.models import *
import sys
import re
from whoosh.fields import *

class Command(BaseCommand):
    
#    option_list = BaseCommand.option_list + (
#        make_option('--verbosity', action='store', dest='verbosity', default='1',
#            type='choice', choices=['0', '1', '2'],
#            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
#        make_option('--noinput', action='store_false', dest='interactive', default=True,
#            help='Tells Django to NOT prompt the user for input of any kind.'),
#    )
#    help = 'Generate work.indexed_title and work.indexed_english_title for all work records.'
#    args = '[appname ...]'

    requires_model_validation = False
    
    def handle(self, *test_labels, **options):
        self.test = False
        #self.update_commentary_sort_orders()
        self.split_synopsis()
        print 'done'
        
    def split_synopsis(self):
        from editions.models import Version
        versions = Version.objects.all().exclude(synopsis='')
        for version in versions:
            synopsis = version.synopsis.strip()
            if len(synopsis) > 5:
                print 'Convert version #%s' % version.id
                # remove all the divs
                synopsis = re.sub(ur'(?musi)</?div[^>]*>', '', synopsis)
                # split around h3
                parts = re.split(ur'<h3[^>]*>', synopsis)
                fields = {}
                for part in parts:
                    # extract the heading (if any)
                    heading = re.sub(ur'(?musi)</h3>.*', '', part)
                    if len(heading) == len(part):
                        heading = ''
                    else:
                        heading = re.sub(ur'(?musi)\s.*', '', heading.strip())
                        if not heading.endswith('s'):
                            heading = heading + 's'
                    rest = re.sub(ur'(?musi).*</h3>', '', part).strip()
                    fields[heading.lower()] = rest
                    #print 'HEADING = %s' % heading.lower()
                attrs = {'synopsis': '', 'print_editions': 'editions', 'synopsis_manuscripts': 'manuscripts'}
                for attr in attrs:
                    existing_value = getattr(version, attr)
                    # we don't overwrite fields with existing values
                    if attr == 'synopsis' or len(existing_value) < 5:
                        val = ''
                        if attrs[attr] not in fields:
                            #print '%s is missing' % attrs[attr]
                            pass
                        else:
                            val = fields[attrs[attr]]
                            del fields[attrs[attr]]
                        #print '%s = %s ' % (attr, self.gs(val))
                        setattr(version, attr, val)
                if fields:
                    print 'WARNING: UNCONVERTED FIELDS: [\'%s\']' % '\', \''.join(fields.keys())
                else:
                    version.save()
                    pass
                #print ('-' * 100)
                #print self.gs(synopsis)
                 
    def writeFile(self, filename, text):
        ret = True
        try:
            f = open(filename, 'w')
            f.write(text.encode('utf-8'))
            f.close()
            ret = True
        except IOError:
            print 'Error writing %s' % filename
        return ret

    def readXMLFile(self, filepath):
        ret = self.readFile(filepath)
        ret = re.sub('<?xml version="1.0"?>', '', ret)
        return ret
        
    def readFile(self, filepath):
        import codecs
        f = codecs.open(filepath, 'r', "utf-8")
        ret = f.read()
        f.close()
        return ret
    
    def replace(self, str, start, length, new):
        return str[:start]+new+str[start+length:]
    
    def warning(self, message):
        war = 'WARNING:' + message
        self.bib_tei = self.bib_tei + '<!--' + war + "-->\n"
        if message not in self.errors:
            self.errors[message] = 0
        self.errors[message] = self.errors[message] + 1
        #print war
        
    def gs(self, str):
        return str.encode('ascii', 'xmlcharrefreplace')
            
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
                    
