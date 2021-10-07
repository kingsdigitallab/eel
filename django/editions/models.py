# -*- coding: utf-8 -*-
# auto generated from an XMI file
from django.db import models
# from models_generic import *
from models_generic import (
    Person, Version, Text_Attribute, Glossary_Term, Work, Commentary,
    Folio_Image, Bibliographic_Entry, Manuscript, Edition,
    Witness_Transcription, Witness_Translation, Edition_Translation, Witness,
    Editor, EEL_Edition_Status, Language, Bib_Category, Archive,
    Sigla_Provenance, Folio_Side, Version_Relationship_Type,
    Version_Relationship, Place, Topic, Hyparchetype, Resource, User_Comment,
    Text_Attribute_Work, Editor_Edition, Bibliographic_Entry_Bib_Category,
    Version_Witness, Witness_Language, Version_Language,
    Edition_Bibliographic_Entry, King
)
from django.conf import settings
import htmlentitydefs
import re
from django.template.defaultfilters import slugify

# Comments about record display names
#
# method                 place where it is used                                                    type of representation
#-------------------------------------------------------------------------
# __unicode__            various places in django, including the heading for the change page       (compact, discriminant)
# __unicode__            in the Foreign Key drop down on the change page
# __unicode__            in the auto-complete text-box
# get_list_name          in the auto-complete drop-down                                            (full description, discriminant)
# get_reference_name     in the default reference inserted by the auto-complete into a text field  (compact, not discriminant)
# (get_short_name)

# BIBLIOGRAPHIC ENTRY


def bibliographic_entry_save(self, force_insert=False, force_update=False):
    # replace <i> with <em>
    # self.styled_reference = re.sub(r'<(/?)i>', r'<\1em>', self.styled_reference).strip()
    # strip any other tag than <em> or <p>
    # self.styled_reference = re.sub(r'<(?!/em>|/p>|em>|p>)[^>]+>', '', self.styled_reference).strip()
    self.styled_reference = re.sub(r'\n', '', self.styled_reference).strip()

    from django.utils.html import strip_tags

    # set the record fields from the marked-up elements in the bibliographic entry
    # author(s)
    # editor(s)
    items = re.findall(
        ur'<span class="tei-author">(.*?)</span>',
        self.styled_reference)
    if len(items) == 0:
        items = re.findall(
            ur'<span class="tei-editor">(.*?)</span>',
            self.styled_reference)
    if len(items) > 0:
        self.authors = strip_tags(items[0])
    else:
        self.authors = ''

    # title (m)
    self.title_monograph = strip_tags(
        ', '.join(
            re.findall(
                ur'<span class="tei-title teia-level__m">(.*?)</span>',
                self.styled_reference)))
    # title (a)
    self.title_article = strip_tags(
        ', '.join(
            re.findall(
                ur'<span class="tei-title teia-level__a">(.*?)</span>',
                self.styled_reference)))
    # date
    dates = re.findall(
        ur'<span class="tei-date">(.*?)</span>',
        self.styled_reference)
    if len(dates):
        self.publication_date = re.sub(ur'\D.*', '', strip_tags(dates[-1]))
    else:
        self.publication_date = None

    # set the creation date
    if self.id is None:
        from datetime import date
        self.created = date.today()

    # bib_info = get_info_from_bib_entry(self.styled_reference)
    # self.title = bib_info['title']
    # self.authors = bib_info['author']
    # self.publication_date = bib_info['date']
    super(Bibliographic_Entry, self).save(force_insert, force_update)


Bibliographic_Entry.save = bibliographic_entry_save


def bibliographic_entry_get_reference_name(self):
    ret = u'(%s' % re.sub('\s*,.*$', '', self.authors)

    if (self.publication_date):
        ret += u" %s" % self.publication_date

    ret += ')'

    return ret


def bibliographic_entry_unicode(self):
    return self.title_article + u' ' + \
        bibliographic_entry_get_reference_name(self)


def bibliographic_entry_get_list_name(self):
    return u'' + re.sub(r'\n|\r', '',
                        re.sub(r'<[^>]*>', '', self.styled_reference))


Bibliographic_Entry.get_list_name = bibliographic_entry_get_list_name
Bibliographic_Entry.get_reference_name = bibliographic_entry_get_reference_name
Bibliographic_Entry.__unicode__ = bibliographic_entry_unicode

# ARCHIVE

Archive._meta.ordering = ['name', 'city']


def archive_entry_unicode(self):
    return u'%s, %s' % (self.name, self.city)


Archive.__unicode__ = archive_entry_unicode

# MANUSCRIPT

Manuscript._meta.ordering = ['shelf_mark', 'archive']


def manuscript_unicode(self):
    return "%s (%s)" % (self.shelf_mark, self.sigla)


Manuscript.__unicode__ = manuscript_unicode


def manuscript_save(self, force_insert=False, force_update=False):
    # SLUGIFY: first name + last name
    self.slug = slugify(self.sigla)
    super(Manuscript, self).save(force_insert, force_update)


Manuscript.save = manuscript_save


def manuscript_get_type_label(self):
    ret = 'manuscript'
    if self.standard_edition:
        ret = 'edition'
    return ret


Manuscript.get_type_label = manuscript_get_type_label


def manuscript_get_double_pages(self):
    # TODO: this should be cached
    images = Folio_Image.objects.filter(
        manuscript=self).order_by('display_order')
    ret = []
    import copy
    # organise the items into a sequence of pairs

    empty_pair = {'0': None, '1': None, 'id': '', 'label': ''}
    #current_pair = copy.deepcopy(empty_pair)
    current_pair = None
    # ret.append(current_pair)
    last_display_order = 0

    for image in images:
        # we remove archived and duplicate images
        if (image.display_order > 0) and not image.archived and (
                image.display_order > last_display_order):
            info = image.get_folio_info()
            if info is not None:
                if (info['side'] == 1) or (current_pair is None) or (current_pair['0'] is None) or (
                        (current_pair['0'].display_order + 1) != image.display_order):
                    # create a new pair
                    current_pair = copy.deepcopy(empty_pair)
                    ret.append(current_pair)
                current_pair[str(1 - info['side'])] = image
                if current_pair['id'] == '':
                    current_pair['id'] = image.id
                # Ensures that only one image with that order appears.
                last_display_order = image.display_order

        #last_display_order = image.display_order

    return ret


Manuscript.get_double_pages = manuscript_get_double_pages


def manuscript_get_witnesses(self):
    ret = Witness.objects.filter(manuscript=self)
    # sort by folio number
    from cch.datastr.strnatcmp import strnatcmp
    ret = sorted([w for w in ret], key=lambda w: str(
        w.range_start), cmp=strnatcmp)
    return ret


Manuscript.get_witnesses = manuscript_get_witnesses


def manuscript_is_single_sheet(self):
    return self.single_sheet


Manuscript.is_single_sheet = manuscript_is_single_sheet

# WORK

Work._meta.ordering = ['name']

# VERSION


def version_save(self, force_insert=False, force_update=False):
    # SLUGIFY: first name + last name
    self.slug = slugify(self.standard_abbreviation)
    super(Version, self).save(force_insert, force_update)


Version.save = version_save


def version_version_name(self):
    ret = self.name
    if ret is None or len(ret) == 0:
        ret = self.work.name
    return ret


Version.version_name = version_version_name


def version_unicode(self):
    return u'%s - %s' % (self.standard_abbreviation, self.version_name())


Version.__unicode__ = version_unicode

Version._meta.ordering = ['standard_abbreviation', ]


def version_get_languages(self):
    return [i.language for i in Version_Language.objects.filter(version=self)]


Version.get_languages = version_get_languages


def version_get_witnesses(self):
    return [w for w in Witness.objects.filter(
        version=self).order_by('manuscript__sigla')]


Version.get_witnesses = version_get_witnesses


def version_get_an_edition(self, show_all=False):
    '''
    Return an edition from a version.
    By default only returns editions with status =
    edition_accepted, ready for review, public.
    If show_all is True, returns any edition linked to
    this version.
    '''
    ret = None
    recs = Edition.objects.filter(
        version=self)
    if not show_all:
        recs = recs.filter(
            eel_edition_status__id__in=[
                5,
                7,
                8
            ]
        )
    if recs.count():
        ret = recs[0]
    return ret


Version.get_an_edition = version_get_an_edition


def version_get_a_king(self):
    ret = None
    if self.work and self.work.king:
        ret = self.work.king
    return ret


Version.get_a_king = version_get_a_king


def version_get_a_language(self):
    ret = None
    languages = self.get_languages()
    if len(languages) == 0:
        ret = Language.objects.get(id=1)
    else:
        ret = languages[0]
    return ret


Version.get_a_language = version_get_a_language


def version_has_filiation(self):
    from django.db.models import Q
    rels = Version_Relationship.objects.filter(Q(source=self) | Q(target=self))
    return (rels.count() > 0)


Version.has_filiation = version_has_filiation


def version_get_graph(self):
    import simplejson as json
    ret = None
    if self.graph is not None and len(self.graph.strip()) > 0:
        ret = json.loads(self.graph)
    return ret


Version.get_graph = version_get_graph


def version_set_graph(self, graph):
    import simplejson as json
    if graph is None:
        graph = ''
    else:
        graph = json.dumps(graph)
    self.graph = graph


Version.set_graph = version_set_graph

# FOLIO_IMAGE


class FolioImageManager(models.Manager):

    class meta:
        model = Folio_Image

    def bulkNaturalFileNameSortOrder(self, using=None):
        # sort all the items based on the filename -> .file_name_sort_order
        from cch.datastr.strnatcmp import strnatcmp
        queryset = self.using(using).all()
        folios = sorted([f for f in queryset],
                        key=lambda f: str(f.filename), cmp=strnatcmp)
        i = 1
        for folio in folios:
            changed = not (folio.filename_sort_order == i)
            folio.filename_sort_order = i
            i = i + 1
            if changed:
                folio.save(using=using)
        return queryset.count()

    def bulkNaturalDisplayOrderSorting(self, using=None):
        # sort all the items based on the page/folio number and side -> .display_order
        # it does not overwrite the display order set manually, unless the page/folio number and side are valid
        # the order is between [1000,2000] and relative to the manuscript
        folios = self.using(using).all()

        for folio in folios:
            info = folio.get_folio_info()

            if info is not None:
                order = get_order_from_folio_info(info)
                changed = not (folio.display_order == order)
                folio.display_order = order
                if changed:
                    folio.save(using=using)


Folio_Image.objects = FolioImageManager()
Folio_Image.objects.contribute_to_class(Folio_Image, 'objects')


def folio_image_get_image_url(self, file_type='jpg'):
    # returns the image url RELATIVE to djatoka server
    # e.g file://path/to/image.jp2
    ret = ''
    if file_type == 'jpg' or file_type == 'jp2':
        file_path = re.sub('\.jpg$', '.jp2', self.filepath)
        #file_path = self.filepath
        ret = '%s/%s' % (settings.EEL_IMAGE_BASE_URL, file_path)
    return ret


Folio_Image.get_image_url = folio_image_get_image_url


def folio_image_get_image_url_full(self, width=0, height=0):
    # returns the image url RELATIVE to djatoka server
    # e.g file://path/to/image.jp2
    ret = self.get_image_url()
    # print ret
    if ret:
        if 0:
            # djatoka
            from templatetags.tags_editions import djatoka_encode
            ret = settings.IMAGE_SERVER_URL + '?url_ver=Z39.88-2004&rft_id=' + \
                djatoka_encode(
                    ret) + '&svc_id=info:lanl-repo/svc/getRegion&svc_val_fmt=info:ofi/fmt:kev:mtx:jpeg2000&svc.format=image/jpeg'
            if width or height:
                ret = ret + '&svc.scale=%s,%s' % (width, height)
        else:
            # loris
            sizes = ','.join([str(s or '') for s in [width, height]])
            ret = r'%s/%s/full/%s/0/default.jpg' % (
                settings.IMAGE_SERVER_URL,
                ret,
                sizes
            )

    return ret


Folio_Image.get_image_url_full = folio_image_get_image_url_full


def folio_image_get_display_location(self, no_prefix=False):
    ''' return 'f.48r'
        if [no_prefix] is False, the location is prefixed with the unit: f. / p.'''
    ret = 'n/a'
    if self.folio_number:
        if no_prefix:
            ret = ''
        else:
            ret = 'f.'
        ret = ret + self.folio_number
        if self.folio_side.id == 3:
            ret = ret + 'r'
        if self.folio_side.id == 4:
            ret = ret + 'v'
    else:
        if self.page:
            if no_prefix:
                ret = ''
            else:
                ret = 'p.'
            ret = ret + self.page

    return ret


Folio_Image.get_display_location = folio_image_get_display_location


def folio_image_get_folio_info(self):
    # returns a dictionary: {'number': integer, 'side': 0=r/1=v, 'page': False=folio/True=page}
    # returns None if invalid
    ret = {'number': 0, 'side': 0, 'page': False}

    # folio or page number, 0 if not valid
    ret['number'] = self.folio_number.strip()
    if ret['number'] == '':
        ret['number'] = self.page
        if ret['number'] != '':
            ret['page'] = True
    if ret['number'] != '':
        try:
            ret['number'] = int(ret['number'])
        except Exception:
            ret['number'] = 0
    else:
        ret['number'] = 0

    # at this point: number = 0 if invalid, > 0 otherwise

    if ret['number'] != 0:
        if ret['page']:
            ret['side'] = (ret['number'] + 1) % 2
        else:
            # r = 0, v = 1, others = -1
            convert_side_number = {3: 0, 4: 1, 5: 0}
            ret['side'] = self.folio_side.id
            if ret['side'] in convert_side_number:
                ret['side'] = convert_side_number[ret['side']]
            else:
                ret['side'] = -1
                ret['number'] = 0

    if ret['number'] == 0:
        ret = None
    return ret


Folio_Image.get_folio_info = folio_image_get_folio_info

# TEXT_ATTRIBUTE
Text_Attribute._meta.ordering = ['name', ]

# BIB_CATEGORIES
Bib_Category._meta.ordering = ['name', ]

# WORK


def work_get_attributes(self):
    return [
        i.text_attribute for i in Text_Attribute_Work.objects.filter(work=self)]


Work.get_attributes = work_get_attributes

# WITNESS


def witness_unicode(self):
    ret = ''
    if self.work is not None:
        ret = ret + self.work.name
    if self.manuscript is not None:
        if len(ret) > 0:
            ret = ret + ' - '
        ret = ret + self.manuscript.sigla
    if len(ret) == 0:
        ret = '{unknown}'
    return ret


Witness.__unicode__ = witness_unicode


def witness_get_versions(self):
    return [
        ref.version for ref in Version_Witness.objects.filter(witness=self)]


Witness.get_versions = witness_get_versions


def witness_is_public(self):
    from django.db.models import Q
    ret = False
    public_status = EEL_Edition_Status.objects.filter(
        Q(name__icontains='public') | Q(name__icontains='online'))
    if public_status.count():
        public_status = public_status[0]
        for version_witness in Version_Witness.objects.filter(witness=self):
            ret = Edition.objects.filter(
                version=version_witness.version,
                eel_edition_status=public_status).count() > 0
            if ret:
                break

    return ret


Witness.is_public = witness_is_public


def witness_contains_folio(self, folio_image):
    ''' Returns True only if the passed Folio_Image contains text from this witness '''
    # TODO: check the compatibility between the format of the folio location
    # and the folio range in the witness.
    ret = False

    if folio_image is not None:
        # compare the the witness range: ['48r'/'48', '55r'] and the folio
        # location: '49'/'prologue', side = Recto
        range_orders = self.get_orders_from_range()
        ret = not (folio_image.display_order <
                   range_orders[0] or folio_image.display_order > range_orders[1])

    return ret


Witness.contains_folio = witness_contains_folio


def witness_get_expanded_range(self):
    ''' Returns an list of folio/page numbers for the range covered by the witness '''
    def s2n(v, d):
        sret = d
        try:
            sret = int(re.sub('\D', '', v))
        except Exception:
            pass
        return sret

    range_num = range(s2n(self.range_start, 1), s2n(self.range_end, 0) + 1)

    if self.page:
        ret = range_num
    else:
        ret = []
        for n in range_num:
            ret.append('%sr' % n)
            ret.append('%sv' % n)
        # exclude first and last if needed
        start = self.range_start
        if len(ret) and len(start) and (start[-1] not in ['r', 'v']):
            start = '%sr' % start
        end = self.range_end
        if len(ret) and len(end) and (end[-1] not in ['r', 'v']):
            end = '%sr' % end
        if len(ret) and (ret[0] != start):
            ret = ret[1:]
        if len(ret) and (ret[-1] != end):
            ret = ret[:-1]

    return ret


Witness.get_expanded_range = witness_get_expanded_range


def witness_get_orders_from_range(self):
    ''' returns a list of image orders from the witness range.
        In case of invalid range format, the orders can be -1 '''
    ret = [
        get_order_from_folio_info(
            get_info_from_location(
                self.range_start, self.page)),
        get_order_from_folio_info(
            get_info_from_location(
                self.range_end, self.page))
    ]
    return ret


Witness.get_orders_from_range = witness_get_orders_from_range


def witness_get_first_available_folio_image(self):
    ret = None
    if self.manuscript is not None:
        range_orders = self.get_orders_from_range()
        folio_images = Folio_Image.objects.filter(manuscript=self.manuscript, display_order__gte=range_orders[0],
                                                  display_order__lte=range_orders[1], archived=False).order_by('display_order')
        if folio_images.count() > 0:
            ret = folio_images[0]
    return ret


Witness.get_first_available_folio_image = witness_get_first_available_folio_image


def witness_get_range_description(self):
    ret = u'%s' % self.range_start
    prefix = 'f.'
    if self.page:
        prefix = 'p.'
    if self.range_start != self.range_end:
        prefix = 'fos.'
        if self.page:
            prefix = 'pp.'
        ret = ret + '-' + self.range_end
    return prefix + ' ' + ret


Witness.get_range_description = witness_get_range_description


def witness_get_languages(self):
    return [i.language for i in Witness_Language.objects.filter(witness=self)]


Witness.get_languages = witness_get_languages


# TODO: turn location/folio_info into a class

def get_order_from_folio_info(info):
    ret = -1
    if info is not None:
        if info['page']:
            ret = info['number']
        else:
            ret = 2 * info['number'] + info['side'] - 1
        ret = ret + 1000
    return ret


def get_info_from_location(location, is_page=False):
    # returns a dictionary: {'number': integer, 'side': 0=r/1=v, 'page': False=folio/True=page}
    # returns None if invalid
    ret = None
    # extract the side from the location
    parts = re.match('(?i)^(\d+)([rv]?)$', location)

    if parts is not None:
        parts = parts.groups()
        if parts is not None and len(parts) == 2:
            ret = {'page': is_page, 'side': 0, 'number': 0}
            # part = ('48', 'r')
            try:
                ret['number'] = int(parts[0])
                if parts[1] == 'v':
                    ret['side'] = 1
            except Exception:
                ret = None

    return ret

# EDITION


def edition_unicode(self):
    return "%s (%s)" % (self.abbreviation, self.version.version_name())


Edition.__unicode__ = edition_unicode


def edition_get_editors(self):
    return [i.editor for i in Editor_Edition.objects.filter(edition=self)]


Edition.get_editors = edition_get_editors


def edition_get_introduction(self):
    from django.utils.html import strip_tags
    ret = self.introduction
    if len(strip_tags(self.introduction)) <= 3:
        ret = self.version.synopsis
    return ret


Edition.get_introduction = edition_get_introduction


def edition_is_public(self):
    return re.match(ur'(?i).*(public|online).*', self.eel_edition_status.name)


Edition.is_public = edition_is_public


def edition_is_listable(self):
    # Ooohh, look! Hard-coded values. That's really poor practice.
    # 5: Edition accepted, 7: Ready for review, 8: Public
    return self.eel_edition_status.id in [5, 7, 8]


Edition.is_listable = edition_is_listable

# EDITION TRANSLATION


def edition_translation_get_edition(self):
    ret = Edition.objects.filter(edition_translation=self)
    if ret.count():
        ret = ret[0]
    else:
        ret = None
    return ret


Edition_Translation.get_edition = edition_translation_get_edition


def edition_translation_unicode(self):
    return u"Translation of %s" % (self.get_edition())


Edition_Translation.__unicode__ = edition_translation_unicode

# PERSON


def person_get_list_name(self):
    ret = self.name
    return ret


def person_get_reference_name(self):
    ret = self.name
    return ret


Person.__unicode__ = person_get_list_name
Person.get_list_name = person_get_list_name
Person.get_reference_name = person_get_reference_name

# PERSON


def place_get_list_name(self):
    ret = self.name
    return ret


def place_get_reference_name(self):
    ret = self.name
    return ret


Place.__unicode__ = place_get_list_name
Place.get_list_name = place_get_list_name
Place.get_reference_name = place_get_reference_name

# HYPARCHETYPES


def hyparchetype_unicode(self):
    ret = self.sigla
    if self.edition:
        ret = self.edition.__unicode__() + ' - ' + ret
    return ret


Hyparchetype.__unicode__ = hyparchetype_unicode

# WITNESS TRANSCRIPTION


def witness_transcription_get_witness(self):
    ret = Witness.objects.filter(witness_transcription=self)
    if ret.count():
        ret = ret[0]
    else:
        ret = None
    return ret


Witness_Transcription.getWitness = witness_transcription_get_witness


def witness_transcription_unicode(self):
    ret = 'Transcription of %s' % self.getWitness().manuscript.sigla
    return ret


Witness_Transcription.__unicode__ = witness_transcription_unicode

# WITNESS TRANSLATION


def witness_translation_get_witness(self):
    return self.get_transcription().getWitness()


Witness_Translation.getWitness = witness_translation_get_witness


def witness_translation_unicode(self):
    ret = 'Translation of %s' % self.getWitness().manuscript.sigla
    return ret


Witness_Translation.__unicode__ = witness_translation_unicode


def witness_translation_get_transcription(self):
    ret = Witness_Transcription.objects.filter(witness_translation=self)
    if ret.count():
        ret = ret[0]
    else:
        ret = None
    return ret


Witness_Translation.get_transcription = witness_translation_get_transcription

# RESOURCES


def resource_unicode(self):
    return u'%s' % (self.title)


Resource.__unicode__ = resource_unicode
Resource.get_list_name = resource_unicode
Resource.get_reference_name = resource_unicode

# GLOSSARY TERM


def glossary_term_list_name(self):
    return u'%s' % (self.term)


Glossary_Term.get_list_name = glossary_term_list_name
Glossary_Term.get_reference_name = glossary_term_list_name

# USER COMMENT


def user_comment_save(self, *args, **kwargs):
    from datetime import datetime
    if not self.id:
        self.timestamp = datetime.now()
    # Call the "real" save() method.
    super(User_Comment, self).save(*args, **kwargs)


User_Comment.save = user_comment_save


def user_comment_get_web_user(self):
    ret = None
    from ugc.models import Web_User
    web_users = Web_User.objects.filter(user__id=self.userid)
    if web_users.count():
        ret = web_users[0]
    return ret


User_Comment.get_web_user = user_comment_get_web_user


def user_comment_text_name(self):
    text = self.get_text()
    return '%s' % text


User_Comment.text_name = user_comment_text_name


def user_comment_get_text(self):
    from django.contrib.contenttypes.models import ContentType
    model = ContentType.objects.get(id=self.content_type).model_class()
    ret = model.objects.get(id=self.objectid)
    return ret


User_Comment.get_text = user_comment_get_text


def user_comment_user_name(self):
    ret = 'None'
    from django.contrib.auth.models import User
    users = User.objects.filter(id=self.userid)
    if users:
        ret = users[0].username
    return ret


User_Comment.user_name = user_comment_user_name


def user_comment_comment_first_words(self):
    l = 30
    ret = self.comment[0:l]
    if len(self.comment) > l:
        ret += '[...]'
    return ret


User_Comment.comment_first_words = user_comment_comment_first_words


def get_clean_html(html_str):
    '''
    Try to clean up the html.
    Convert entities to unicode.
    Remove comments, inline styles, duplicate <doc> at the root level,
    some empty divs and p
    '''

    ret = html_str or ''

    # convert xhtml entities into unicode characters
    # otherwise our python XML parser will complain about undefined entities
    # when you try to load the document
    ret = decode_entities(ret)

    # Remove duplicate nested doc, see Active Collab 34
    # <doc><doc><doc>...</doc></doc></doc> => <doc>...</doc>
    ret = re.sub(ur'(?us)(<doc>\s*)+', u'<doc>', ret)
    ret = re.sub(ur'(?us)(</doc>\s*)+', u'</doc>', ret)

    # Remove styles attributes
    ret = re.sub(ur'''(?us)\bstyle\s*=\s*("[^"]*"|'[^']*')''', u'', ret)
    # Remove comments
    ret = re.sub(ur'''(?us)<!--.*?-->''', u'', ret)

    # remove em and strong
    ret = re.sub(u'(?us)</?(em|strong)>', u'', ret)

    # remove br when they are the only child within a node
    ret = re.sub(u'(?us)(>)\s*<br\s*/>\s*(<)', ur'\1\2', ret)

    # remove empty paragraphs
    ret = re.sub(u'(?us)<(p)>\s*</\1>', u'', ret)

    # remove empty tei divs
    ret = re.sub(
        ur'(?us)<(div|span)\s[^>]*class="tei-div[^"]*"[^>]*>\s*</\1>',
        u'',
        ret)

    # remove empty paragraphs
    ret = re.sub(u'(?us)<p>\s*</p>', u'', ret)

    return ret


def decode_entities(text):
    def fixup(m):
        text = m.group(0)
        c = text
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    c = unichr(int(text[3:-1], 16))
                else:
                    c = unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                c = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        # don't decode xml entities as this could break the xml
        # e.g. <p> 1 &lg; 2 </p>
        if c not in ['"', "'", '&', '<', '>']:
            text = c
        return text
    return re.sub("&#?\w+;", fixup, text)


def get_source_abbreviations():
    '''Returns a dictionary: {witness_apparatus_code: witness_abbreviation}
    Used to decode the references to witnessed in the critical apparatus.
    '''
    ret = {}

    for witness in Witness.objects.all():
        ret['W%d' % witness.id] = witness.manuscript.sigla
    for archetype in Hyparchetype.objects.all():
        ret['A%d' % archetype.id] = archetype.sigla

    return ret


def get_string_from_html_encoded_critical_apparatus(ca, source_abbreviations):
    from urllib import unquote
    import simplejson as json

    # ["4324",["1212","W79"]]
    ca = json.loads(unquote(unquote(str(ca[0])).decode('utf-8')))
    token = ca.pop(0)
    ca = token + u': ' + u', '.join([
        u'"%s" in %s' % (
            reading[0],
            source_abbreviations.get(reading[1], '?'),
        )
        for reading
        in ca
    ])

    ca += '<br/>'

    return ca
