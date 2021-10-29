# Authors: Geoffroy Noel, King's College London, 2009-2020
#
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
        self.test = False
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
#        for archive in Images.objects.all():
#            archive.delete()
#        for manuscript in Manuscript.objects.all():
#            manuscript.delete()
        
        mss_file = self.readFile('convert_data/batch4.txt')
        lines = mss_file.split('\n')
        city = ''
        lc = 0
        lc_max = 100000
        for line in lines:
            lc = lc + 1
            if lc > lc_max and self.test: break
            
            line = line.strip(' \r')
            #print line
            # batch 1 and 2
            #parts = re.match(ur'^\./(batch.+?)-jpg/(.+)/(.+)\.jpg$', line)
            # batch3
            #parts = re.match(ur'^(batch.+?)-jpg/(.+)/(.+)\.jp2$', line)
            # ls (liebermann and stubb)
            #parts = re.match(ur'^([^/]+)/(.+)\.jp2$', line)
            # batch4
            parts = re.match(ur'^(batch.+?)/(.+)/(.+)\.jp2$', line)
            if parts is not None:
                img = self.createImgRecord(line, parts.group(1), parts.group(2), parts.group(3))
                #img = self.createImgRecord(line, 'batch4', '', parts.group(2))
            else:
                print 'WARNING: not recognised (%s)' % line
            
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
        #print fullpath
        # primary data
        fullpath = fullpath.strip()
        batch = batch.strip()
        path = path.strip()
        filename = filename.strip()
        images = Folio_Image.objects.filter(filepath=fullpath)
        if images.count() > 0:
            ret = images[0]
        else:
            ret = Folio_Image()
        print 'IMG %s %s %s %s' % (fullpath, batch, path, filename)
        
        ret.filepath = fullpath
        ret.batch = batch
        ret.path = path
        ret.filename = filename
        if not self.test:
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
        print 'MS %s %s %s %s' % (ret.sigle, ret.shelf_mark)
        if not self.test:
            ret.save()
        return ret
    
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
                    
