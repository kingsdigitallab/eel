# Authors: Geoffroy Noel, King's College London, 2009-2020
#
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
        self.update_commentary_sort_orders()
        self.index_editions()
        self.index_witnesses()
        print 'done'

    def update_commentary_sort_orders(self):
        print 'Sort the commentaries'
        for edition in Edition.objects.all().order_by('id'):
            print '\tedition #%s' % edition.id
            order = 1
            text = edition.text
            if len(text.strip()) > 0:
                # get all the ids from the text
                ids = re.findall('id="([^"]+)"', text)
                commentaries = {}
                for commentary in Commentary.objects.filter(
                        elementid__in=ids, edition=edition):
                    commentaries[commentary.elementid] = commentary
                if len(commentaries) > 0:
                    for id in ids:
                        if id in commentaries:
                            commentaries[id].sort_order = order
                            commentaries[id].save()
                            order = order + 1

            print '\t\t%s commentaries' % (order - 1)

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
        #print war

    def index_editions(self):
        import sys
        import os
        from whoosh.index import create_in
        from whoosh.analysis import StemmingAnalyzer
        from django.utils.html import strip_tags

        stem_ana = StemmingAnalyzer()

        schema = Schema(title=TEXT(stored=False, analyzer=stem_ana),
                        recid=ID(stored=True),
                        text=TEXT(stored=True),
                        translation=TEXT(stored=True, analyzer=stem_ana),
                        abbreviation=TEXT(stored=False),
                        editors=TEXT(stored=False),
                        attributes=TEXT(stored=False, analyzer=stem_ana),
                        commentary=TEXT(stored=True, analyzer=stem_ana),
                        )
        # clear the index
        ix = create_in(
            os.path.join(
                settings.PROJECT_FILEPATH,
                'indices'),
            schema,
            'edition')

        writer = ix.writer()

        editions = Edition.objects.all().order_by('id')
        i = 0
        for edition in editions:
            print '\t%s' % edition.id
            print u'\t\t%s (%s)' % (repr(edition.abbreviation), repr(edition.version.standard_abbreviation))
            if not edition.is_listable():
                print '\t\tNOT LISTABLE ****************'
                continue
            i = i + 1
            translation = edition.edition_translation

            text_translation = u''
            if (translation is not None) and edition.is_public():
                text_translation = strip_tags(translation.text)

            text = u''
            if (edition.text is not None) and edition.is_public():
                text = strip_tags(edition.text)

            eds = ur' '.join([u'%s %s' % (a.first_name, a.last_name)
                              for a in edition.get_editors()])
            print '\t\t%s' % repr(eds)

            attributes = ur' '.join([u'%s' % a.name.strip()
                                     for a in edition.version.work.get_attributes()])

            commentary = u''
            if edition.is_public():
                commentary = ur' '.join([strip_tags(c.text) for c in Commentary.objects.filter(
                    edition=edition).order_by('sort_order')])

            print '\t\t%s' % (self.gs(edition.version.version_name()), )

            writer.add_document(title=edition.version.version_name(),
                                recid=u'%s' % edition.id,
                                text=self.clean_text(text),
                                translation=self.clean_text(text_translation),
                                abbreviation=edition.version.standard_abbreviation,
                                editors=eds,
                                attributes=attributes,
                                commentary=commentary,
                                )

        writer.commit()

        print 'Indexed %d editions.' % i

    def gs(self, str):
        return repr(str)

    def index_witnesses(self):
        import sys
        import os
        from whoosh.index import create_in
        from whoosh.analysis import StemmingAnalyzer
        from django.utils.html import strip_tags

        stem_ana = StemmingAnalyzer()

        schema = Schema(
            title=TEXT(stored=False),
            shelf_mark=TEXT(stored=False),
            work_name=TEXT(stored=False),
            recid=ID(stored=True),
            transcription=TEXT(stored=True),
            translation=TEXT(stored=True, analyzer=stem_ana),
            sigla=ID(stored=True),
            editors=TEXT(stored=False),
            attributes=TEXT(stored=False, analyzer=stem_ana),
        )
        # clear the index
        ix = create_in(
            os.path.join(
                settings.PROJECT_FILEPATH,
                'indices'),
            schema,
            'witness')

        writer = ix.writer()

        witnesses = Witness.objects.all().order_by('id')
        i = 0
        for witness in witnesses:
            print '\t%s' % witness.id
            i = i + 1
            transcription = witness.witness_transcription
            text_transcription = u''
            if (transcription is not None) and witness.is_public():
                text_transcription = strip_tags(transcription.text)

            translation = None
            if transcription and transcription.witness_translation:
                translation = transcription.witness_translation
            text_translation = u''
            if (translation is not None) and witness.is_public():
                text_translation = strip_tags(translation.text)

            # manuscript
            title = u''
            sigla = u''
            shelf_mark = u''
            if witness.manuscript:
                sigla = u'%s' % witness.manuscript.sigla
                shelf_mark = u'%s' % witness.manuscript.shelf_mark
                title = title + witness.manuscript.sigla + ' ' + witness.manuscript.shelf_mark
                if witness.manuscript.archive:
                    title = title + ' ' + witness.manuscript.archive.name + \
                        ' ' + witness.manuscript.archive.city

            # work
            work_name = u''
            attributes = ur''
            if witness.work:
                work_name = witness.work.name
                attributes = ur' '.join([u'%s' % a.name.strip()
                                         for a in witness.work.get_attributes()])

            #eds = ur' '.join([u'%s %s' % (a.first_name, a.last_name) for a in edition.get_editors()])

#            vi = 0
#            for v in [title, work_name, witness.id, text_transcription, text_translation, sigla, u'', attributes]:
#                print vi
#                print v.__class__.__name__
#                vi = vi + 1

            print '\t\t%s\n\t\t%s\n\t\t%s' % (self.gs(title), self.gs(work_name), self.gs(text_translation[1:20]))

            writer.add_document(
                title=title,
                work_name=work_name,
                shelf_mark=shelf_mark,
                recid=u'%s' % witness.id,
                transcription=self.clean_text(text_transcription),
                translation=self.clean_text(text_translation),
                sigla=sigla,
                editors=u'',
                attributes=attributes,
            )

        writer.commit()

        print 'Indexed %d witnesses.' % i

    def clean_text(self, text):
        ret = re.sub(r'\[[^]]*\]', '', text)
        return ret

    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
