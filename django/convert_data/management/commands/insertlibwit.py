from django.core.management.base import BaseCommand
from optparse import make_option
from eel.editions.models import *
import sys
import re
import urllib2
from graphlayout.graph import Graph
from graphlayout.layout import Layout
from django.db.models import Q
from datetime import date, timedelta
import math


class Command(BaseCommand):
    '''
        Insert the witnesses corresponding to Liebermann and Stubbs.
        The witnesses are not insert twice.
        The information is read from the printed editions field in the version record. 
    '''
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
    
    def __init__(self):
        pass
    
    def handle(self, *test_labels, **options):
        self.insertLiebermannWitnesses()
        print 'done'

    def insertLiebermannWitnesses(self):
        standard_editions = [[u'Angelsachsen', 'liebermann'], [u'Select Charters and Other Illustrations', 'stubbs']]
        
        for standard_edition in standard_editions:
            manuscripts = Manuscript.objects.filter(sigla__iexact=standard_edition[1])
            if manuscripts.count() == 0:
                print 'ERROR: could not find Ms with sigla = %s' % standard_edition[1]
                return
            standard_edition.append(manuscripts[0])
        
        # 1. scan all the bibliographical info in the versions
        for version in Version.objects.all().order_by('id'):
            entries = version.print_editions
            if entries and len(entries) > 4:
                print version.id
                for standard_edition in standard_editions:
                    #print self.gs(entries)
                    pages = re.sub(u'(?musi).*%s.*?p\.\s*([\d\u2013]+).*' % standard_edition[0], ur'\1', entries)
                    if len(pages) == len(entries):
                        #print '\tNO FOUND'
                        pass
                    else:
                        pages = re.split(u'\u2013', pages)
                        for i in range(0, len(pages)):
                            try:
                                pages[i] = int(pages[i])
                            except:
                                break
                        #print pages
                        if len(pages) == 1:
                            pages.append(pages[0])
                        if pages[1] < pages[0]: 
                            pages[1] = ('%s' % pages[0])[:len('%s' % pages[0]) - len('%s' % pages[1])] + '%s' % pages[1]
                            
                        #print pages
                    
                        new_rec = False
                        witnesses = Witness.objects.filter(version=version, manuscript=standard_edition[2])
                        if witnesses.count() == 0:
                            witness = Witness()
                            new_rec = True
                            print '\tcreate new witness.'
                        else:
                            witness = witnesses[0]                    
                        witness.work = version.work
                        witness.range_start = pages[0]
                        witness.range_end = pages[1]
                        witness.page = True
                        witness.hide_from_listing = False
                        witness.manuscript = standard_edition[2]
                        witness.save()
                        
                        if new_rec:
                            witness_version = Version_Witness()
                            witness_version.witness = witness
                            witness_version.version = version
                            witness_version.save()                        
    
                            languages = Version_Language.objects.filter(version=version)
                            for language in languages:
                                witness_language = Witness_Language()
                                witness_language.witness = witness
                                witness_language.language = language.language
                                witness_language.save()
                    
                        print '\t%s, pp. %s-%s, wit #%s' % (standard_edition[1], pages[0], pages[1], witness.id)

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
        
    def reFind(self, pattern, string):
        ret = None
        items = re.findall(pattern, string)
        if len(items) > 0:
            ret = items[0]
        return ret
            
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret

    def gs(self, str):
        return str.encode('ascii', 'xmlcharrefreplace')
