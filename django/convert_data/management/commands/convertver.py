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
        self.ver_count = 0
        self.parseVersions()

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
        
    def parseVersions(self):
#        for record in Version.objects.all():
#            record.delete()
#        for manuscript in Manuscript.objects.all():
#            manuscript.delete()
        
        mss_file = self.readFile('convert_data/versions.txt')
        lines = mss_file.split('\n')
        i = 0
        for line in lines:
            line = line.strip(' \r')
            parts = line.split('\t')
            #parts = re.match(ur'^\./(batch.+?)-jpg/(.+)/(.+)\.jpg$', line)
            if len(parts) > 1:
                i = i + 1
                print i
                version = self.createVersionRecord(parts)
            
#            mg1 = re.match('^\t(.+)$', line)
#            if mg1 is not None:
#                city = mg1.group(1)
#            else:
#                parts = line.split('\t')
#                
#                msno = parts[0].strip()
#                sigla = parts[2].strip()
#                
#                msinfo = parts[1]
#                #msparts = msinfo.split('MS')
#                msparts = re.match('(?i)(.*?)(MS .*?)(fos\.|pp\.|p\.|fo\..*)', msinfo)
#                
#                if msparts is not None:
#                    library = msparts.group(1).strip()
#                    msname = msparts.group(2).strip()
#                    #self.createRecords(msno, sigla, msname, library, city)
#                    print library
#                    print msname
#                else:
#                    print '** MS or fos. not found'

    def createVersionRecord(self, parts):
        #print parts
        # primary data
        abbreviation = parts[0].strip()
        print abbreviation

        # create or find the record
        versions = Version.objects.filter(standard_abbreviation=abbreviation)
        if versions.count() > 0:
            ret = versions[0]
        else:
            ret = Version(standard_abbreviation=abbreviation)
        # name
        ret.name = parts[1].strip()

        # sets the laguage
        language = parts[2].strip()
        if re.match('(?ui)French', language): language = 'Old French'
        if re.match('(?ui)English', language): language = 'Old English'
        languages = Language.objects.filter(name=language)
        if languages.count() == 0:
            #print 'NOT FOUND %s %s' % (language, abbreviation)
            language = Language.objects.get(id=1)
        else:
            language = languages[0]
        ret.language = language

        # find or create the work
        works = Work.objects.filter(name=ret.name)
        if works.count() > 0:
            work = works[0]
        else:
            work = Work(name=ret.name)
        work.save()
        
        # link the version to the work
        ret.work = work

        # save the version
        ret.save()

        return ret
    
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
                    
