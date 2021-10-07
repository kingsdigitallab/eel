# * DESCRIPTION
# * 
# * Author: geoffroy.noel@kcl.ac.uk
# * 19 Mar 2010
# *
# * ref: http://www.tei-c.org/Guidelines/P4/html/CO.html#COBI
# *
# */
import re

class BibParser(): 
    
    def init(self):
        import os, sys
        self.errors = {}
        prj_path = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath( __file__ )), '..'))
        prj_parent_path = os.path.normpath(os.path.join(prj_path, '..'))
        module_name = os.path.basename(prj_path)
        
        def add_path(p): 
            if p not in sys.path: sys.path.append(p)
        add_path(prj_parent_path)
        add_path(prj_path)
        os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % module_name
    
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
    
    def markup_authors(self, start, end, str):
        if end > start:
            role = 'author'
            # get the authors fragment
            authors = str[start:end]
            #print '[%s]' % authors
            # ignore the bits that we know are not author names
            authors = re.sub('\(eds?.\).*', '', authors)
            if len(authors) < end-start:
                role = 'editor'
            authors = re.sub('(?:\W)and(?:\W)', ',', authors)
            authors = re.sub('(?:<i>)?\s*et al\.\s*(?:</i>)?', '', authors)
            authors = authors.rstrip(u', \u2018')
            authors = authors.lstrip(u'\u2019 ,')
            authors = re.sub('^in\s', '', authors)
            authors = re.findall('(?:^|,)([^,.]+,[^,]+)', authors)
            part = str[start:end]
            for author in authors:
                part = part.replace(author, '<%s>%s</%s>' % (role, author, role), 1);
            str = self.replace(str, start, end - start, part)
        return str
    
    def findAllWithPos(self, pattern, str, start=0, end=-1):
        ''' returns an array or triple. each triple corresponds to a match of [pattern] in [str].
            a triple is made of (match, pos_start, pos_end) '''
        ret = []
        if end == -1: end = len(str) + 1
        str = str[start:end]

        for m in re.finditer(pattern, str):
            ret.append([m.group(1), start + m.start(), start + m.end()])
        
        return ret

    def warning(self, message):
        war = 'WARNING:' + message
        self.bib_tei = self.bib_tei + '<!--' + war + "-->\n"
        if message not in self.errors:
            self.errors[message] = 0
        self.errors[message] = self.errors[message] + 1
        #print war
        
    def parseBib(self):
        self.init()
        self.bib_tei = ''
        insert_db = True
        #f = self.readXMLFile('bib-source.out-short.xml');
        f = self.readXMLFile('bib-source.out.xml');
        
        from eel.editions.models import Bibliographic_Entry, Bib_Category, Bibliographic_Entry_Bib_Category, Language
        language_english = Language.objects.filter(name='Modern English')
        language_english = language_english[0]
        
        biblines = re.findall(r'<bibl>(.*?)<\/bibl>', f);
        cat = ''
        for bibline in biblines:
            ''' we take the last bit in italics in the entry as the title of the monograph '''
            italics = re.findall(r'(?u)<i>.*?<\/i>', bibline)
            index_title_m = len(bibline)
            title_m = ''
            if italics:
                title_m = italics[-1]
                if (re.search(ur'et al\.', title_m) is None):
                    index_title_m = bibline.rfind(title_m)
                    new_title = '<title level="m">%s</title>' % title_m;
                    bibline = self.replace(bibline, index_title_m, len(title_m), new_title)
                                
            ''' we take the bit before the monograph title and surrounded by quotation marks as the title of the article '''
            index_title_a = 0
            index_title_a_end = 0
            title_a = ''
            a_titles = re.findall(u'(?u),\s*\u2018(.*)\u2019\s*,', bibline[:index_title_m])
            if a_titles:
                # todo: search in a smaller window: stops at the date
                title_a = a_titles[0]
                index_title_a = (bibline[:index_title_m]).rfind(title_a)
                new_title = r'<title level="a">%s</title>' % title_a
                bibline = self.replace(bibline, index_title_a, len(title_a), new_title)
                index_title_a_end = index_title_a + len(new_title)

            ''' we take the 1234) after all titles as the publication date '''
            after_titles = bibline.rfind('</title>')
            if after_titles == -1:
                after_titles = 0
            bibline = bibline[:after_titles] + re.sub(ur'(?u)(\d{4}(?:(?:-|\u2013)\d{1,2})?)\)', r'<date>\1</date>)', bibline[after_titles:])

            ''' if no article title and no date, this line must be a category '''
            if not italics and not a_titles and bibline.find('<date>') == -1:
                cat = bibline
                print 'CATEGORY: %s' % cat
                continue

            ''' we mark up the authors/editors before the first title '''
            bibline = self.markup_authors(0, bibline.find('<title'), bibline)
            if title_m == '':
                ''' we mark up the authors/editors between the two titles'''
                begin = bibline.find('</title>') + 8
                end = bibline.find('<title', begin)
                if end != -1:
                    bibline = self.markup_authors(begin, end, bibline)

            #print bibline

            #
            author = ''
            authors = re.findall('<author>(.*?)</author>', bibline)
            if authors:
                author = authors[0]
            else:
                authors = re.findall('<editor>(.*?)</editor>', bibline)
                if authors:
                    author = authors[0]
            date = ''
            dates = re.findall('<date>(.*?)</date>', bibline)
            if dates:
                date = dates[0]
            
            if title_m == '':
                self.warning('could not detect monograph title.')
            if author == '':
                self.warning('could not detect author.')
            if date == '':
                self.warning('could not detect date.')

            # add the line to the TEI document 
            self.bib_tei = self.bib_tei + "<bibl>%s</bibl>\n" % bibline;

            # convert TEI -> XHTML/TEI
            bibline = re.sub(u'<(\w{2,})>', ur'<span class="tei-\1">', bibline);
            bibline = re.sub(u'</(\w{2,})>', r'</span>', bibline);
            bibline = re.sub(u'<title level="([^"]*)">', ur'<span class="tei-title teia-level__\1">', bibline)
            
            # insert category in the database
            
            if insert_db:            
                categories = Bib_Category.objects.filter(name = cat)
                if categories.count() == 0:
                    category = Bib_Category()
                    category.name = cat
                    category.save()
                else:
                    category = categories[0]
                
                # insert the entry in the database
                
                date = re.sub(u'\D.*', '', date)
                if date == '1903':
                    yo = 0
                    yo = 2
                if date:
                    entries = Bibliographic_Entry.objects.filter(publication_date = date, authors = author)
                    if entries.count() == 0:
                        entry = Bibliographic_Entry()
                    else:
                        entry = entries[0]
                    entry.styled_reference = '<div class="tei-bibl">'+bibline+'</div>'
                    entry.language = language_english
                    entry.save()
                    
                    entry_cats = Bibliographic_Entry_Bib_Category.objects.filter(bibliographic_entry = entry, bib_category = category)
                    if entry_cats.count() == 0:
                        entry_cat = Bibliographic_Entry_Bib_Category()
                        entry_cat.bibliographic_entry = entry
                        entry_cat.bib_category = category
                        entry_cat.save()
            
            #print bibline
        
        self.bib_tei = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI>
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title>Bib sample</title>
                <author>Geoffroy Noel</author>
            </titleStmt>
            <publicationStmt>
                <p>freely available</p>
            </publicationStmt>
            <sourceDesc>
                <p>Written from scratch.</p>
            </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
            <listBibl>
                <head>Bibliography</head>
                %s
                </listBibl>
        </body>
    </text>
    %s
</TEI>''' % (self.bib_tei, self.report_errors()) 
        self.writeFile('bib-tei.xml', self.bib_tei)
        
        print self.report_errors()
        
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
                    
parser = BibParser()
parser.parseBib()
