from django.core.management.base import BaseCommand
from optparse import make_option
from eel.editions.models import *
import sys
import re
import urllib2

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
        self.importSynopsis()

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
        
    def importSynopsis(self):
#        for record in Version.objects.all():
#            record.delete()
#        for manuscript in Manuscript.objects.all():
#            manuscript.delete()

        # read text list page
        #versions = self.getWebPage('http://eel-local.cch.kcl.ac.uk/laws/texts.html')
        #self.writeFile('versions.html', versions)
        versions = self.readFile('versions.html')
        #lines  = re.search('href\s*=\s*"synopsis/([^"]+)\.html"', versions)
        #print re.findall(ur'(?isum)<td class="c01">([^<]*)</td>\s+<td.*?href\s*=\s*"synopsis/([^"]+)\.html".*?</td>', versions)
        for row in re.findall(ur'(?isum)<tr.*?</tr>', versions):
            abbrv = self.reFind(ur'(?isum)<td class="c01">([^<]+)</td>', row)
            if abbrv is None: continue
            page_name = self.reFind(ur'(?isum)href\s*=\s*"synopsis/([^"]+)\.html"', row)
            if page_name is None: continue
            versions = Version.objects.filter(standard_abbreviation=abbrv)
            print abbrv
            if versions.count() > 0:
                version = versions[0]
                url = 'http://eel-local.cch.kcl.ac.uk/laws/synopsis/%s.html' % page_name
                page = self.getWebPage(url)
                if page is None:
                    print '\tWARNING: page not found %s' % url
                    continue
                # get the mainContent div
                content = self.reFind('(?isum)<div\s+id="mainContent">.*?</h1>.*?<div.*?(<p.*?)</div>\s*?</div>\s*?</td>', page)
                if content is None:
                    print '\tWARNING: could not extract content' % url
                    continue
                # clean the content from the polluting namespaces
                content = re.sub('xmlns=".*?"', '', content)
                version.synopsis = content
                version.save()
            else:
                print '\tWARNING: abbreviation not in the database'
            #exit()
        
        #lines  = re.match(ur'href\s*=\s*"synopsis/([^"]+)\.html"', list_page)
        #lines  = re.match(ur'href', list_page)
        #print list_page
        #print lines.groups()
        #print list_page
                
#        mss_file = self.readFile('convert_data/versions.txt')
#        lines = mss_file.split('\n')
#        for line in lines:
#            line = line.strip(' \r')
#            parts = line.split('\t');
#            #print line
#            #print line
#            #parts = re.match(ur'^\./(batch.+?)-jpg/(.+)/(.+)\.jpg$', line)
#            if len(parts) > 1:
#                version = self.createVersionRecord(parts)
        
    def reFind(self, pattern, string):
        ret = None
        items = re.findall(pattern, string)
        if len(items) > 0:
            ret = items[0]
        return ret
            
    def createVersionRecord(self, parts):
        print parts
        # primary data
        abbreviation = parts[0].strip()
        versions = Version.objects.filter(standard_abbreviation=abbreviation)
        if versions.count() > 0:
            ret = versions[0]
        else:
            ret = Version(standard_abbreviation=abbreviation)
        ret.name = parts[1].strip()
        ret.save()
        
        return ret
    
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret

        
    def getWebPage(self, url):
        #url = 'http://www.acme.com/products/3322'
        ret = None
        try:
            req = urllib2.Request(url)
            #req.add_header('Accept-Charset', 'utf-8')
            raw_response = urllib2.urlopen(req)
            ret = raw_response.read()
            ret = unicode(ret, 'utf-8')
#            if self.latin1_in_unicode:
#                self.response = unicode(self.response, 'iso-8859-1')
        except Exception, e:
            #self.setError(u'%s' % e, self.MUP_ERROR_CODE_GENERIC, e.__class__.__name__)
            pass
        return ret
    
