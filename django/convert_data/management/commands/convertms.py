from django.core.management.base import BaseCommand
from optparse import make_option
from eel.editions.models import *
import sys
import re

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
        self.parseMS()

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
        
    def parseMS(self):
#        for archive in Archive.objects.all():
#            archive.delete()
#        for manuscript in Manuscript.objects.all():
#            manuscript.delete()
        
        mss_file = self.readFile('convert_data/manuscripts.txt')
        lines = mss_file.split('\n')
        city = ''
        for line in lines:
            line = line.strip(' \r')
            print line
            mg1 = re.match('^\t(.+)$', line)
            if mg1 is not None:
                city = mg1.group(1)
            else:
                parts = line.split('\t')
                
                msno = parts[0].strip()
                sigla = parts[2].strip()
                
                msinfo = parts[1]
                #msparts = msinfo.split('MS')
                msparts = re.match('(?i)(.*?)(MS .*?)(fos\.|pp\.|p\.|fo\..*)', msinfo)
                
                if msparts is not None:
                    library = msparts.group(1).strip()
                    msname = msparts.group(2).strip()
                    self.createRecords(msno, sigla, msname, library, city)
                    print library
                    print msname
                else:
                    print '** MS or fos. not found'

    def createRecords(self, msno, sigla, msname, library, city):
        archive = self.createArchive(library, city)
        ret = self.createMS(msno, sigla, msname, archive)
        return ret
    
    def createArchive(self, library, city):
        library = library.strip(', ')
        city = city.strip()
        archives = Archive.objects.filter(city=city, name=library)
        if archives.count() > 0:
            ret = archives[0]
        else:
            ret = Archive(city=city, name=library, country='England')
            ret.save()
        return ret
        
    def createMS(self, msno, sigla, msname, archive):
        #msno =
        sigla = sigla.strip()
        msname = msname.strip('* ')
        ms = Manuscript.objects.filter(shelf_mark=msname)
        if ms.count() > 0:
            ret = ms[0]
            print '--------------- ALREADY EXISTS'
        else:
            ret = Manuscript(sigla=sigla, shelf_mark=msname)
            ret.archive = archive
            ret.save()
        return ret
    
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
                    
