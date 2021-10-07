# -*- coding: utf-8 -*-
# auto generated from an XMI file
from django.db import models

from cch.fuzzydate import fields

from django.utils.encoding import force_unicode

# Referenced by a foreign key
import django.contrib.auth.models


def getUnicode(obj):
    if (obj is None):
        return u""
    else:
        return force_unicode(obj)


#
class Person(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Version(models.Model):
    standard_abbreviation = models.CharField(
        max_length=32, null=False, default="", blank=False, )
    synopsis = models.XMLField(null=False, default="", blank=True, )
    name = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=True,
        help_text=ur'''Leave empty if the name is the same as the Law's name.''',
    )
    slug = models.SlugField(max_length=250, )
    print_editions = models.XMLField(null=False, default="", blank=True, )
    synopsis_manuscripts = models.XMLField(
        null=False, default="", blank=True, )
    date = fields.FuzzyDateField(null=True, modifier=True, blank=True, )
    graph = models.TextField(null=False, default="", blank=True, )
    work = models.ForeignKey('Work', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        unique_together = (('standard_abbreviation', ),)

    def __unicode__(self):
        return getUnicode(self.standard_abbreviation)

    table_group = ''


#
class Text_Attribute(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Text Attribute'
        verbose_name_plural = 'Text Attributes'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Glossary_Term(models.Model):
    term = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )
    description = models.XMLField(null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Glossary Term'
        verbose_name_plural = 'Glossary Terms'
        unique_together = (('term', ),)

    def __unicode__(self):
        return getUnicode(self.term)

    table_group = 'Edition'


#
class Work(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    date = fields.FuzzyDateField(null=True, modifier=True, blank=True, )
    text_attribute = models.ManyToManyField(
        'Text_Attribute',
        blank=False,
        null=False,
        default=1,
        through='Text_Attribute_Work',
    )
    king = models.ForeignKey('King', blank=True, null=True, )

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = ''


#
class Commentary(models.Model):
    text = models.XMLField(null=False, default="", blank=True, )
    user = models.ForeignKey(
        django.contrib.auth.models.User,
        help_text=ur'''User (editor or registered user) who submitted this comment.''',
    )
    elementid = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )
    updated = models.DateTimeField(null=True, blank=True, )
    sort_order = models.IntegerField(null=True, blank=True, )
    edition = models.ForeignKey(
        'Edition',
        blank=False,
        null=False,
        default=1,
    )

    class Meta:
        verbose_name = 'Commentary'
        verbose_name_plural = 'Commentaries'

    table_group = 'Edition'


#
class Folio_Image(models.Model):
    filename = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=True,
    )
    filepath = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    batch = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )
    folio_number = models.CharField(
        max_length=8,
        null=False,
        default="",
        blank=True,
        help_text=ur'''Folio number. Leave empty if unknown. Do not include the r/v information.''',
    )
    page = models.CharField(
        max_length=8,
        null=False,
        default="",
        blank=True,
        help_text=ur'''Archive page number. Leave empty if not available.''',
    )
    display_order = models.IntegerField(
        null=True,
        blank=True,
        help_text=ur'''Optional. This number indicates in which order this folio will appear in a sequential reading of the manuscript. The value is relative to the display order of the other folio images.''',
    )
    internal_notes = models.CharField(
        max_length=1024, null=False, default="", blank=True, )
    path = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=True,
    )

    filename_sort_order = models.IntegerField(
        null=True,
        blank=True,
        help_text=ur'''= natsort(filename), used to sort the records by filename in the list view.''',
    )
    archived = models.BooleanField(default=False, null=False, blank=False, )
    manuscript = models.ForeignKey(
        'Manuscript', blank=False, null=False, default=1, )
    folio_side = models.ForeignKey(
        'Folio_Side', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'Folio Image'
        verbose_name_plural = 'Folio Images'
        unique_together = (('filepath', ),)

    def __unicode__(self):
        return getUnicode(self.filepath)

    table_group = 'Manuscripts'


#
class Bibliographic_Entry(models.Model):
    styled_reference = models.XMLField(null=False, default="", blank=True, )
    authors = models.CharField(
        max_length=255,
        null=False,
        default="",
        blank=True,
    )
    title_article = models.CharField(
        max_length=1024, null=False, default="", blank=True, )
    title_monograph = models.CharField(
        max_length=1024, null=False, default="", blank=True, )
    publication_date = models.IntegerField(null=True, blank=True, )
    created = models.DateField(null=True, blank=True, )
    language = models.ForeignKey(
        'Language', blank=False, null=False, default=1, )
    edition = models.ManyToManyField(
        'Edition',
        blank=True,
        null=True,
        through='Edition_Bibliographic_Entry',
    )

    class Meta:
        verbose_name = 'Bibliographic Entry'
        verbose_name_plural = 'Bibliographic Entries'

    table_group = 'Bibliographic references'


#
class Manuscript(models.Model):
    shelf_mark = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    description = models.XMLField(null=False, default="", blank=True, )
    sigla = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )
    slug = models.SlugField(max_length=250, )
    hide_from_listings = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text=ur'''Hide from the manuscript listings on the website as it is a late text and so not an artifact of early English law by itself.''',
    )
    checked_folios = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text=ur'''Tick this box if the facsimiles of this manuscript have been verified and are ready to be displayed on the public website.''',
    )
    single_sheet = models.BooleanField(
        default=False, null=False, blank=False, )
    hide_folio_numbers = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text=ur'''Tick this box if the folio or page numbers should not appear on the website. To appear on the website, all folio images must have a folio or page number assign to them in the datatabase. When the folios have no real/actual number this requirement forces you to provide abritrary numbers anyway. In that case, ticking this box will hide this arbitrary number on the site.''',
    )
    standard_edition = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text=ur'''Tick this box if this document is a standard edition (e.g. Liebermann, Stubbs).''',
    )
    archive = models.ForeignKey(
        'Archive',
        blank=False,
        null=False,
        default=1,
    )
    sigla_provenance = models.ForeignKey(
        'Sigla_Provenance', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'Manuscript'
        verbose_name_plural = 'Manuscripts'
        unique_together = (('shelf_mark', ),)

    def __unicode__(self):
        return getUnicode(self.shelf_mark)

    table_group = 'Manuscripts'


#
class Edition(models.Model):
    date_of_edition = fields.FuzzyDateField(
        null=True, modifier=True, blank=True, )
    text = models.XMLField(null=False, default="", blank=True, )
    abbreviation = models.CharField(
        max_length=32, null=False, default="", blank=True, )
    internal_notes = models.TextField(
        null=False,
        default="",
        blank=True,
        help_text=ur'''Internal notes associated to this edition. They will not appear on the website.''',
    )
    introduction = models.XMLField(null=False, default="", blank=True, )
    rendered_edition = models.XMLField(null=False, default="", blank=True, )
    rendered_translation = models.XMLField(
        null=False, default="", blank=True, )
    rendered_commentary = models.XMLField(null=False, default="", blank=True, )
    rendered_apparatus = models.XMLField(null=False, default="", blank=True, )
    editor = models.ManyToManyField(
        'Editor',
        blank=False,
        null=False,
        default=1,
        through='Editor_Edition',
    )
    eel_edition_status = models.ForeignKey(
        'EEL_Edition_Status', blank=False, null=False, default=1, )
    edition_translation = models.ForeignKey(
        'Edition_Translation', blank=True, null=True, )
    version = models.ForeignKey(
        'Version',
        blank=False,
        null=False,
        default=1,
    )

    class Meta:
        verbose_name = 'Edition'
        verbose_name_plural = 'Editions'

    table_group = 'Edition'


#
class Witness_Transcription(models.Model):
    text = models.XMLField(null=False, default="", blank=True, )
    rendered_text = models.XMLField(null=False, default="", blank=True, )
    witness_translation = models.ForeignKey(
        'Witness_Translation', blank=True, null=True, )

    class Meta:
        verbose_name = 'Witness Transcription'
        verbose_name_plural = 'Witness Transcriptions'

    table_group = 'Law text in a manuscript'


#
class Witness_Translation(models.Model):
    text = models.XMLField(null=False, default="", blank=True, )
    rendered_text = models.XMLField(null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Witness Translation'
        verbose_name_plural = 'Witness Translations'

    table_group = 'Law text in a manuscript'


#
class Edition_Translation(models.Model):
    text = models.XMLField(null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Edition Translation'
        verbose_name_plural = 'Edition Translations'

    table_group = 'Edition'


#
class Witness(models.Model):
    range_start = models.CharField(
        max_length=8,
        null=False,
        default="",
        blank=True,
        help_text=ur'''The page/folio number in the source document that correspond to the beginning of the text. (e.g. '10' or '30r')''',
    )
    range_end = models.CharField(
        max_length=8,
        null=False,
        default="",
        blank=True,
        help_text=ur'''The page/folio number in the source document that correspond to the end of the text. (e.g. '15' or '41v')''',
    )
    description = models.XMLField(null=False, default="", blank=True, )
    medieval_translation = models.BooleanField(
        default=False, null=False, blank=False, )
    page = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text=ur'''Tick this box if the range is expressed in page numbers. Leave it unticked if the range is expressed in folio numbers.''',
    )
    hide_from_listings = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text=ur'''Hide from the manuscript listings on the website as it is a late text and and so not artifact of early English law by itself.''',
    )
    rendered_facsimiles = models.XMLField(null=False, default="", blank=True, )
    manuscript = models.ForeignKey(
        'Manuscript', blank=False, null=False, default=1, )
    work = models.ForeignKey('Work', blank=False, null=False, default=1, )
    version = models.ManyToManyField(
        'Version',
        blank=False,
        null=False,
        default=1,
        through='Version_Witness',
    )
    witness_transcription = models.ForeignKey(
        'Witness_Transcription', blank=True, null=True, )

    class Meta:
        verbose_name = 'Witness'
        verbose_name_plural = 'Witnesses'

    table_group = 'Law text in a manuscript'


#
class Editor(models.Model):
    first_name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )
    abbreviation = models.CharField(
        max_length=32, null=False, default="", blank=False, )
    last_name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )

    class Meta:
        verbose_name = 'Editor'
        verbose_name_plural = 'Editors'
        unique_together = (('abbreviation', ),)

    def __unicode__(self):
        return getUnicode(self.abbreviation)

    table_group = 'Edition'


#
class EEL_Edition_Status(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'EEL Edition Status'
        verbose_name_plural = 'EEL Edition Statuses'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class King(Person):
    beginning_regnal_year = fields.FuzzyDateField(
        null=True, modifier=True, blank=True, )
    end_regnal_year = fields.FuzzyDateField(
        null=True, modifier=True, blank=True, )

    class Meta:
        verbose_name = 'King'
        verbose_name_plural = 'Kings'

    table_group = 'Auth. List'


#
class Language(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )
    color = models.CharField(
        max_length=8,
        null=False,
        default="",
        blank=True,
    )
    witness = models.ManyToManyField(
        'Witness',
        blank=True,
        null=True,
        through='Witness_Language',
    )
    version = models.ManyToManyField(
        'Version',
        blank=True,
        null=True,
        through='Version_Language',
    )

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Bib_Category(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    bibliographic_entry = models.ManyToManyField(
        'Bibliographic_Entry',
        blank=True,
        null=True,
        through='Bibliographic_Entry_Bib_Category',
    )

    class Meta:
        verbose_name = 'Bib Category'
        verbose_name_plural = 'Bib Categories'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Bibliographic references'


#
class Archive(models.Model):
    country = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=True,
    )
    city = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    name = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Archive'
        verbose_name_plural = 'Archives'
        unique_together = (('city', 'name', ),)

    def __unicode__(self):
        return getUnicode(self.city) + ', ' + getUnicode(self.name)

    table_group = 'Manuscripts'


#
class Sigla_Provenance(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Sigla Provenance'
        verbose_name_plural = 'Sigla Provenances'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Folio_Side(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Folio Side'
        verbose_name_plural = 'Folio Sides'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Version_Relationship_Type(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    description = models.XMLField(null=False, default="", blank=True, )

    class Meta:
        verbose_name = 'Version Relationship Type'
        verbose_name_plural = 'Version Relationship Types'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Work Relationships'


#
class Version_Relationship(models.Model):
    description = models.XMLField(null=False, default="", blank=True, )
    target = models.ForeignKey(
        'Version',
        blank=False,
        null=False,
        default=1,
        related_name='%(class)s_target',
    )
    source = models.ForeignKey(
        'Version',
        blank=False,
        null=False,
        default=1,
        related_name='%(class)s_source',
    )
    version_relationship_type = models.ForeignKey(
        'Version_Relationship_Type', blank=False, null=False, default=1, )

    class Meta:
        verbose_name = 'Version Relationship'
        verbose_name_plural = 'Version Relationships'

    table_group = 'Work Relationships'


#
class Place(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Topic(models.Model):
    name = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=False,
    )

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        unique_together = (('name', ),)

    def __unicode__(self):
        return getUnicode(self.name)

    table_group = 'Auth. List'


#
class Hyparchetype(models.Model):
    sigla = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )
    description = models.CharField(
        max_length=1024,
        null=False,
        default="",
        blank=True,
    )
    edition = models.ForeignKey(
        'Edition',
        blank=False,
        null=False,
        default=1,
    )

    class Meta:
        verbose_name = 'Hyparchetype'
        verbose_name_plural = 'Hyparchetypes'

    table_group = 'Auth. List'


#
class Resource(models.Model):
    title = models.CharField(
        max_length=128,
        null=False,
        default="",
        blank=False,
    )
    caption = models.CharField(
        max_length=255,
        null=False,
        default="",
        blank=True,
    )
    file = models.FileField(upload_to='uploads', )

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    table_group = 'Resources'


#
class User_Comment(models.Model):
    userid = models.IntegerField(null=True, blank=True, )
    comment = models.XMLField(null=False, default="", blank=True, )
    content_type = models.IntegerField(null=True, blank=True, )
    objectid = models.IntegerField(null=True, blank=True, )
    division = models.CharField(
        max_length=32,
        null=False,
        default="",
        blank=True,
    )
    private = models.BooleanField(default=False, null=False, blank=False, )
    archived = models.BooleanField(default=False, null=False, blank=False, )
    timestamp = models.DateTimeField(null=True, blank=True, )
    editionid = models.IntegerField(null=True, blank=True, )

    class Meta:
        verbose_name = 'User Comment'
        verbose_name_plural = 'User Comments'

    table_group = ''


# Many To Many Tables

#
class Text_Attribute_Work(models.Model):
    text_attribute = models.ForeignKey('Text_Attribute')
    work = models.ForeignKey('Work')

#


class Editor_Edition(models.Model):
    editor = models.ForeignKey('Editor')
    edition = models.ForeignKey('Edition')

#


class Bibliographic_Entry_Bib_Category(models.Model):
    bibliographic_entry = models.ForeignKey('Bibliographic_Entry')
    bib_category = models.ForeignKey('Bib_Category')

#


class Version_Witness(models.Model):
    version = models.ForeignKey('Version')
    witness = models.ForeignKey('Witness')

#


class Witness_Language(models.Model):
    witness = models.ForeignKey('Witness')
    language = models.ForeignKey('Language')

#


class Version_Language(models.Model):
    version = models.ForeignKey('Version')
    language = models.ForeignKey('Language')

#


class Edition_Bibliographic_Entry(models.Model):
    edition = models.ForeignKey('Edition')
    bibliographic_entry = models.ForeignKey('Bibliographic_Entry')

    # association fields
    page_ranges = models.CharField(
        max_length=32, null=False, default="", blank=True, )
