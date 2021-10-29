# -*- coding: utf-8 -*-
# Authors: Geoffroy Noel, King's College London, 2009-2020
#
from django.core.management.base import BaseCommand
from optparse import make_option
# from editions.models import *
from editions.models import (
    Commentary, Edition, Folio_Image, Witness, Hyparchetype,
    Witness_Transcription, Witness_Translation, get_clean_html,
    get_source_abbreviations)
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
        self.render_facsimiles()
        self.render_editions()
        self.render_witnesses()
        end_line = 'Done.'
        if self.test:
            end_line += ' (TEST MODE)'
        else:
            end_line += ' (WRITE MODE)'
        print end_line

    def render_witnesses(self):
        for record in Witness_Translation.objects.all().order_by('id'):
            print 'Witness translation %d' % record.id
            record.rendered_text = self.get_rendered_text(record)
            record.save()
        for record in Witness_Transcription.objects.all().order_by('id'):
            print 'Witness transcription %d' % record.id
            record.rendered_text = self.get_rendered_text(record)
            record.save()

    def render_editions(self):
        for edition in Edition.objects.all().order_by('id'):
            #             if not edition.id == 40:
            #                 continue
            print u'\tedition #%s %s' % (edition.id, repr(edition.abbreviation))
            order = 1

            # edition text
            id_info = {}
            edition.rendered_edition = self.get_rendered_text(
                edition, id_info, edition, True)

            # translation
            edition.rendered_translation = ''
            if edition.edition_translation:
                edition.rendered_translation = self.get_rendered_text(
                    edition.edition_translation)

            # commentary
            self.render_commentary(edition, id_info)

            # user comments
            self.render_user_comments(edition, id_info)

            # critical apparatus
            self.render_critical_apparatus(edition, id_info)

            edition.save()

    def get_rendered_text(self, record, id_info={},
                          edition=None, is_edition=False):
        text = get_clean_html(record.text)

        # strip off all the explicit chapterisation, e.g. '[Prol. 1]'
        ret = self.strip_explicit_chapterisation(text)
        ret = self.insert_anchors(ret, id_info, edition, is_edition, record)

        # remove polluting doc elements surrounding the text
        ret = re.sub(ur'(?i)</?doc>', '', ret)
        ret = re.sub(
            ur'(<span\b[^>]*\bcch-sup\b[^>]*>)([^<]*)(<\/span>)',
            ur'\1[\2]\3',
            ret)
        # make sure we have s single root element
        ret = '<div>%s</div>' % ret

        # ret2 = re.findall(ur'(?imu)<span class="cch-pb tei-pb
        # teia-witid__(\d+) teia-loc__(\w+)">', ret)

        # transform the page breaks
        # <span class="cch-pb tei-pb teia-witid__61 teia-loc__147v">[PB]</span>
        # =>
        # <span id="a-#p#-p-61_147v" class="anchor anchor-p anchor-p-61">[PB]</span>
        ret = re.sub(ur'(?imu)<span class="cch-pb tei-pb teia-witid__(\d+) teia-loc__(\w+)">(.*?)</span>',
                     ur'<span id="a-#p#-p-\1_\2" class="anchor anchor-p anchor-p-\1"><span class="anchor-label anchor-label-p">\3</span></span>', ret)

        return ret

    def insert_anchors(self, text, id_info, edition=None,
                       is_edition=False, record=None):
        '''
        * Converts arbitrary ids into id which contain information about the hierarchical level of the element.
        * Insert chapter labels and anchors.
        * Insert commentary labels and anchors.
        * Populate id_info with id_info[originalid] = {'new_id': 'a-#p#-c-0-0-p-0-2', 'label': 'Prol 2'}
        '''
        from editions.text_views import get_divs_tree, get_dom_from_text
        text_dom = get_dom_from_text(text)
        tree = get_divs_tree(text_dom, False, None, [])
        l_ret = {'ret': text}
        l_ret['ret'] = re.sub(
            'tei-div',
            'tei-div anchor anchor-c',
            l_ret['ret'])

        from django.contrib.contenttypes.models import ContentType
        recordid = record.id
        record_content_typeid = ContentType.objects.get_for_model(
            record.__class__).id

        commentaries = {}
        if edition:
            for commentary in Commentary.objects.filter(edition=edition):
                commentaries[commentary.elementid] = commentary

        div_orders = {
            'code': {'order': 0, 'prefix': ''},
            'book': {'order': 1, 'prefix': ''},
            'chapter': {'order': 2, 'prefix': 'c_'},
            'prologue': {'order': 2, 'prefix': 'p_'},
        }

        def parse_dic(dic):
            if 'children' in dic:
                child_index = 0
                for child in dic['children']:

                    new_n = dic['n'][:]

                    prefix = ''
                    order = -1

                    if child['type'] in div_orders:
                        order = div_orders[child['type']]['order']
                        prefix = div_orders[child['type']]['prefix']
                        # truncates new_n
                        new_n = new_n[:order]
                        # extends new_n
                        while (len(new_n) < order):
                            new_n.append('0')

                    new_n.append('%s%s' % (prefix, child['n']))
                    child['n'] = new_n

                    # process the kids and pass them the current 'n' as an array
                    # print child
                    parse_dic(child)

                    # convert the array to a dotted string
                    divid = '_'.join(child['n'])
                    child['n'] = 'a-#p#-c-' + divid

                    # print child['n']

                    div_label = self.get_division_label(new_n)
                    if 'id' in child:
                        id_info[child['id']] = {
                            'new_id': child['n'], 'label': div_label}
                    div_commentary = ''

                    div_user_comments = ''
                    # We skip the UC anchor for the first division in a chapter/prologue otherwise we would have '[UC][UC]' in the text.
                    # The first UC would be the prologue/chapter and the second the first division within this chapter.
                    # if is_edition and ((child_index > 0) or (child['type'] !=
                    # 'division')):
                    if ((child_index > 0) or (child['type'] != 'division')):
                        div_user_comments = ur'<span id="a-#p#-uc-%s-r-%s-%s" class="anchor-label anchor-label-uc anchor anchor-uc">[UC]</span>' % (
                            divid, record_content_typeid, recordid)

                    if div_label:
                        div_label = ur'<span class="anchor-label anchor-label-c">[' + \
                            div_label + ']</span>'
                        if 'id' in child and child['id'] in commentaries:
                            div_commentary = ur'<span id="a-#p#-co-%s" class="anchor-label anchor-label-co">[co]</span>' % commentaries[
                                child['id']].id
                            # print ''  + child['id'] + ' ' + div_commentary
                    l_ret['ret'] = re.sub(
                        ur'"' +
                        child['id'] +
                        '"([^>]*>(\s*<(?:p|div)>)?)',
                        ur'"' +
                        child['n'] +
                        ur'"\1' +
                        div_label +
                        div_commentary +
                        div_user_comments,
                        l_ret['ret'])

                    child_index += 1

                    # print len(l_ret['ret'])

                    # print child['n']

        # print tree
        # tree['n'] = 'a-#p#-c-'
        tree['n'] = []
        parse_dic(tree)

        if not self.test:
            # print tree
            pass
        return l_ret['ret']

    def get_division_label(self, div_seq):
        # [u'1', '0', u'c_2', u'11', u'1']
        from roman import fromroman, toroman
        ret = ''
        if len(div_seq) < 4:
            # either, code, book, chapter or prologue
            if len(div_seq) == 1:
                # TODO:
                #ret = 'Code %s' % div_seq[0]
                ret = ''
            if len(div_seq) == 2:
                ret = 'Book %s' % toroman(int(div_seq[0]))
            if len(div_seq) == 3:
                parts = div_seq[2].split('_')
                if len(parts) == 2:
                    # TODO: not really consistent.
                    # Number not visible when only one prologue
                    if parts[0] == 'p':
                        ret = 'Prologue'
                    else:
                        ret = '%s' % parts[1]
        else:
            # anything under chapter or prologue
            parts = div_seq[2].split('_')
            # TODO: not really consistent.
            # TODO: a and b... for third level
            # Number not visible when only one prologue
            if len(parts) == 2:
                if parts[0] == 'p':
                    if div_seq[3] != '0':
                        ret = 'Prol. ' + div_seq[3]
                else:
                    if div_seq[3] != '0':
                        ret = parts[1] + '.' + div_seq[3]
        return ret

    def strip_explicit_chapterisation(self, text):
        return re.sub(ur'(?i)\[(\d|prol)[^]]*\]', '', text)

    def render_facsimiles(self):
        width = 0
        height = 200
        for witness in Witness.objects.all().order_by('id'):
            print '\twitness #%s' % witness.id
            order = 0
            facsimile_html = u''

            range = witness.get_orders_from_range()
            images = Folio_Image.objects.filter(
                manuscript__witness=witness).filter(
                display_order__range=range).order_by('display_order')
            for image in images:
                facsimile_html += u'''<div id="a-#p#-p-%s_%s" class="facsimile anchor anchor-p anchor-p-%s">
                                        <div class="lazy-image" style="height:%dpx;">
                                            <span>%s</span>
                                        </div>
                                        <p class="anchor-label anchor-label-p">
                                            %s
                                        </p>
                                    </div>\n''' % (
                    witness.id,
                    image.get_display_location(True),
                    witness.id,
                    height,
                    image.get_image_url_full(width, height),
                    image.get_display_location()
                )
            order = images.count()

            facsimile_html = '''<div class="facsimiles">
                                %s
                                </div>''' % facsimile_html

            witness.rendered_facsimiles = facsimile_html
            if not self.test:
                witness.save()
            else:
                if witness.rendered_facsimiles:
                    # print witness.rendered_facsimiles
                    pass
#
            if order > 0:
                print '\t\t%s images' % order

    def render_user_comments(self, edition, id_info):
        pass

    def render_commentary(self, edition, id_info):
        # print '\tedition #%s' % edition.id
        order = 1
        text = get_clean_html(edition.text)
        commentary_text = u''
        if len(text.strip()) > 0:
            # get all the ids from the text
            ids = re.findall('id="([^"]+)"', text)
            commentaries = {}
            for commentary in Commentary.objects.filter(
                    elementid__in=id_info.keys(), edition=edition).order_by('id'):
                commentaries[commentary.elementid] = commentary
            if len(commentaries) > 0:
                for id in ids:
                    if id in commentaries:
                        entry = re.sub(
                            ur'(?imu)^\s*<p>(.*)</p>\s*$',
                            ur'\1',
                            commentaries[id].text)
                        commentary_text = commentary_text + \
                            u'''
                                <p id="a-#p#-co-%s" class="anchor anchor-co">
                                    <span id="%s" class="anchor anchor-c anchor-label anchor-label-c">[%s]</span>
                                    %s
                                </p>
                                ''' % \
                            (commentaries[id].id, id_info[id]
                             ['new_id'], id_info[id]['label'], entry)
                        order = order + 1
        edition.rendered_commentary = commentary_text
        if not self.test:
            edition.save()

        if (order - 1) > 0:
            print '\t\t%s commentaries' % (order - 1)

    def render_critical_apparatus(self, edition=None, id_info={}):
        from urllib import unquote
        import simplejson as json

        # dictionary to translate references to source in the CA to the
        # sigla of the corresponding MS or hyparchetype
        source_abbreviations = get_source_abbreviations()

        order = 0
        text = get_clean_html(edition.text)
        apparatus_text = u''
        if len(text.strip()) > 0:
            # get all the ids from the text
            '''
            findall extracts pairs:
            (
                u'<span class="cch-app tei-app teia-readings__%5B%22ac%22,%5B%22et%22,%22A7%22%5D%5D">[A]</span>',
                u'%5B%22ac%22,%5B%22et%22,%22A7%22%5D%5D'
            )
            Then we decode the second element:
            ["ac",["et","A7"]]
            And render it:
            Where A7 stands for archetype nb 7, W61 would be witness record 61
            =>
            ac] reading1 MS1 MS2; reading2 MS3
            '''

            elements = re.findall(ur'<(?:div|span)[^>]*>', text)

            ca_id = 1
            chapter_anchor = ''
            for element in elements:
                id = re.findall(ur'id="([^"]+)"', element)
                if len(id):
                    id = id[0]
                    if id in id_info:
                        chapter_anchor = '<div id="%s" class="anchor anchor-c anchor-label anchor-label-c">[%s]</div>' % (
                            id_info[id]['new_id'],
                            id_info[id]['label']
                        )
                apparatus = re.findall(
                    '(?u)(<span[^>]+teia-readings__([^"]+)[^>]+>)', element)
                if len(apparatus):
                    # u'%5B%22%C3%BE%C3%A6t%20%22,%5B%227%22,%22W79%22%5D%5D'
                    # => '["\xc3\xbe\xc3\xa6t ",["7","W79"]]'
                    apparatus = unquote(str(apparatus[0][1]))
                    # => u'["þæt ",["7","W79"]]'
                    apparatus = u'%s' % apparatus.decode('utf-8')
                    # => ["þæt ", ["7", "W79"]]
                    apparatus = json.loads(unquote(apparatus))
                    apparatus_html = u'%s]' % apparatus[0]
                    for i in range(1, len(apparatus)):
                        if i > 1:
                            apparatus_html += u';'
                        apparatus_html += u' %s' % apparatus[i][0]
                        for source_code in apparatus[i][1:]:
                            abbreviation = u'?'
                            if source_code in source_abbreviations:
                                abbreviation = source_abbreviations[source_code]
                            apparatus_html += u' %s' % abbreviation

                    # {om} => <span class="ca-em">om</span>
                    apparatus_html = re.sub(
                        ur'{([^}]+)}',
                        ur'<span class="ca-em">\1</span>',
                        apparatus_html)

                    ca_id = ca_id + 1
                    ca_id_html = u'a-#p#-ca-%s' % ca_id
                    apparatus_text = apparatus_text + u'''
                        %s
                        <p id="%s" class="anchor anchor-ca">
                            %s
                        </p>''' % (
                        chapter_anchor,
                        ca_id_html,
                        apparatus_html,
                    )
                    chapter_anchor = ''
                    edition.rendered_edition = edition.rendered_edition.replace(
                        element, '<span id="%s" class="anchor-label anchor-label-ca">' % ca_id_html)

        edition.rendered_edition = re.sub(
            ur'(<span[^>]+anchor-label-ca"[^>]*>).*?(</span>)',
            ur'\1&dagger;\2',
            edition.rendered_edition)
        edition.rendered_apparatus = apparatus_text
        if not self.test:
            edition.save()

        if order > 0:
            print '\t\t%s apparatus.' % order

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
        return str[:start] + new + str[start + length:]

    def warning(self, message):
        war = 'WARNING:' + message
        self.bib_tei = self.bib_tei + '<!--' + war + "-->\n"
        if message not in self.errors:
            self.errors[message] = 0
        self.errors[message] = self.errors[message] + 1
        # print war

    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
