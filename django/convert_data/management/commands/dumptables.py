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
    
    def handle(self, *tables, **options):
        # mysqldump --complete-insert --no-create-info -u root -p eel -t editions_version > eel.sql
        try:
            import settings
        except ImportError, e:
            print e
            print "ERROR: settings.py not found in the current directory\n"

        if len(tables) == 0:
            print 'You need to pass at least one table name.'
            exit()

        host = settings.DATABASE_HOST
        if host != '':
            host = '-h %s' % host
        tables = ' '.join(tables)
        command = 'mysqldump -u %s --complete-insert --no-create-info --single-transaction --password="%s" %s %s -t %s > %s.sql' % (settings.DATABASE_USER, settings.DATABASE_PASSWORD, host, settings.DATABASE_NAME, tables, settings.DATABASE_NAME);
        self.run_command(command)

    def run_command(self, command):
        import os
        ret = os.system(command)
        return ret

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
#        for archive in Images.objects.all():
#            archive.delete()
#        for manuscript in Manuscript.objects.all():
#            manuscript.delete()
        
        mss_file = self.readFile('convert_data/images.txt')
        lines = mss_file.split('\n')
        city = ''
        for line in lines:
            line = line.strip(' \r')
            #print line
            parts = re.match(ur'^\./(batch.+?)-jpg/(.+)/(.+)\.jpg$', line)
            if parts is not None:
                img = self.createImgRecord(line, parts.group(1), parts.group(2), parts.group(3))
            
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

    def createImgRecord(self, fullpath, batch, path, filename):
        print fullpath
        # primary data
        fullpath = fullpath.strip()
        batch = batch.strip()
        path = path.strip()
        filename = filename.strip()
        images = Folio_Image.objects.filter(filepath=fullpath)
        if images.count() > 0:
            ret = images[0]
        else:
            ret = Folio_Image(filepath=fullpath,batch=batch,path=path,filename=filename)
            ret.save()
        
        # derived data
        #ret.
        
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
                    
