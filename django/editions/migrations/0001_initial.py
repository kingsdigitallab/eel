# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('editions_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['Person'])

        # Adding unique constraint on 'Person', fields ['name']
        db.create_unique('editions_person', ['name'])

        # Adding model 'Version'
        db.create_table('editions_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('standard_abbreviation', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('synopsis', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('print_editions', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('synopsis_manuscripts', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('date_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_mod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('date', self.gf('cch.fuzzydate.fields.FuzzyDateField')(modifier=True, null=True, blank=True)),
            ('graph', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Work'])),
        ))
        db.send_create_signal('editions', ['Version'])

        # Adding unique constraint on 'Version', fields ['standard_abbreviation']
        db.create_unique('editions_version', ['standard_abbreviation'])

        # Adding model 'Text_Attribute'
        db.create_table('editions_text_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['Text_Attribute'])

        # Adding unique constraint on 'Text_Attribute', fields ['name']
        db.create_unique('editions_text_attribute', ['name'])

        # Adding model 'Glossary_Term'
        db.create_table('editions_glossary_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('description', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
        ))
        db.send_create_signal('editions', ['Glossary_Term'])

        # Adding unique constraint on 'Glossary_Term', fields ['term']
        db.create_unique('editions_glossary_term', ['term'])

        # Adding model 'Work'
        db.create_table('editions_work', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('date_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_mod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('date', self.gf('cch.fuzzydate.fields.FuzzyDateField')(modifier=True, null=True, blank=True)),
            ('king', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.King'], null=True, blank=True)),
        ))
        db.send_create_signal('editions', ['Work'])

        # Adding unique constraint on 'Work', fields ['name']
        db.create_unique('editions_work', ['name'])

        # Adding model 'Commentary'
        db.create_table('editions_commentary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('elementid', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Edition'])),
        ))
        db.send_create_signal('editions', ['Commentary'])

        # Adding model 'Folio_Image'
        db.create_table('editions_folio_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('filepath', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('batch', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('folio_number', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
            ('page', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('internal_notes', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('filename_sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('manuscript', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Manuscript'])),
            ('folio_side', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Folio_Side'])),
        ))
        db.send_create_signal('editions', ['Folio_Image'])

        # Adding unique constraint on 'Folio_Image', fields ['filepath']
        db.create_unique('editions_folio_image', ['filepath'])

        # Adding model 'Bibliographic_Entry'
        db.create_table('editions_bibliographic_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('styled_reference', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('authors', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('title_article', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('title_monograph', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Language'])),
        ))
        db.send_create_signal('editions', ['Bibliographic_Entry'])

        # Adding model 'Manuscript'
        db.create_table('editions_manuscript', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shelf_mark', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('description', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('hide_from_listings', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('checked_folios', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('single_sheet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide_folio_numbers', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('standard_edition', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Archive'])),
            ('sigla_provenance', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Sigla_Provenance'])),
        ))
        db.send_create_signal('editions', ['Manuscript'])

        # Adding unique constraint on 'Manuscript', fields ['shelf_mark']
        db.create_unique('editions_manuscript', ['shelf_mark'])

        # Adding model 'Edition'
        db.create_table('editions_edition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_of_edition_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_of_edition_mod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('date_of_edition', self.gf('cch.fuzzydate.fields.FuzzyDateField')(modifier=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('internal_notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('introduction', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('rendered_edition', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('rendered_translation', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('rendered_commentary', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('rendered_apparatus', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('eel_edition_status', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.EEL_Edition_Status'])),
            ('edition_translation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Edition_Translation'], null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Version'])),
        ))
        db.send_create_signal('editions', ['Edition'])

        # Adding model 'Witness_Transcription'
        db.create_table('editions_witness_transcription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('rendered_text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('witness_translation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Witness_Translation'], null=True, blank=True)),
        ))
        db.send_create_signal('editions', ['Witness_Transcription'])

        # Adding model 'Witness_Translation'
        db.create_table('editions_witness_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('rendered_text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
        ))
        db.send_create_signal('editions', ['Witness_Translation'])

        # Adding model 'Edition_Translation'
        db.create_table('editions_edition_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
        ))
        db.send_create_signal('editions', ['Edition_Translation'])

        # Adding model 'Witness'
        db.create_table('editions_witness', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('range_start', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
            ('range_end', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
            ('description', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('medieval_translation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide_from_listings', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rendered_facsimiles', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('manuscript', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Manuscript'])),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Work'])),
            ('witness_transcription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Witness_Transcription'], null=True, blank=True)),
        ))
        db.send_create_signal('editions', ['Witness'])

        # Adding model 'Editor'
        db.create_table('editions_editor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
        ))
        db.send_create_signal('editions', ['Editor'])

        # Adding unique constraint on 'Editor', fields ['abbreviation']
        db.create_unique('editions_editor', ['abbreviation'])

        # Adding model 'EEL_Edition_Status'
        db.create_table('editions_eel_edition_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['EEL_Edition_Status'])

        # Adding unique constraint on 'EEL_Edition_Status', fields ['name']
        db.create_unique('editions_eel_edition_status', ['name'])

        # Adding model 'King'
        db.create_table('editions_king', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['editions.Person'], unique=True, primary_key=True)),
            ('beginning_regnal_year_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('beginning_regnal_year_mod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('beginning_regnal_year', self.gf('cch.fuzzydate.fields.FuzzyDateField')(modifier=True, null=True, blank=True)),
            ('end_regnal_year_to', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_regnal_year_mod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('end_regnal_year', self.gf('cch.fuzzydate.fields.FuzzyDateField')(modifier=True, null=True, blank=True)),
        ))
        db.send_create_signal('editions', ['King'])

        # Adding model 'Language'
        db.create_table('editions_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('color', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
        ))
        db.send_create_signal('editions', ['Language'])

        # Adding unique constraint on 'Language', fields ['name']
        db.create_unique('editions_language', ['name'])

        # Adding model 'Bib_Category'
        db.create_table('editions_bib_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
        ))
        db.send_create_signal('editions', ['Bib_Category'])

        # Adding unique constraint on 'Bib_Category', fields ['name']
        db.create_unique('editions_bib_category', ['name'])

        # Adding model 'Archive'
        db.create_table('editions_archive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
        ))
        db.send_create_signal('editions', ['Archive'])

        # Adding unique constraint on 'Archive', fields ['city', 'name']
        db.create_unique('editions_archive', ['city', 'name'])

        # Adding model 'Sigla_Provenance'
        db.create_table('editions_sigla_provenance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['Sigla_Provenance'])

        # Adding unique constraint on 'Sigla_Provenance', fields ['name']
        db.create_unique('editions_sigla_provenance', ['name'])

        # Adding model 'Folio_Side'
        db.create_table('editions_folio_side', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['Folio_Side'])

        # Adding unique constraint on 'Folio_Side', fields ['name']
        db.create_unique('editions_folio_side', ['name'])

        # Adding model 'Version_Relationship_Type'
        db.create_table('editions_version_relationship_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('description', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
        ))
        db.send_create_signal('editions', ['Version_Relationship_Type'])

        # Adding unique constraint on 'Version_Relationship_Type', fields ['name']
        db.create_unique('editions_version_relationship_type', ['name'])

        # Adding model 'Version_Relationship'
        db.create_table('editions_version_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='version_relationship_target', to=orm['editions.Version'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='version_relationship_source', to=orm['editions.Version'])),
            ('version_relationship_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Version_Relationship_Type'])),
        ))
        db.send_create_signal('editions', ['Version_Relationship'])

        # Adding model 'Place'
        db.create_table('editions_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['Place'])

        # Adding unique constraint on 'Place', fields ['name']
        db.create_unique('editions_place', ['name'])

        # Adding model 'Topic'
        db.create_table('editions_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
        ))
        db.send_create_signal('editions', ['Topic'])

        # Adding unique constraint on 'Topic', fields ['name']
        db.create_unique('editions_topic', ['name'])

        # Adding model 'Hyparchetype'
        db.create_table('editions_hyparchetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sigla', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['editions.Edition'])),
        ))
        db.send_create_signal('editions', ['Hyparchetype'])

        # Adding model 'Resource'
        db.create_table('editions_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('caption', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('editions', ['Resource'])

        # Adding model 'User_Comment'
        db.create_table('editions_user_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.XMLField')(default='', blank=True)),
            ('content_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('division', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('editionid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('editions', ['User_Comment'])

        # Adding model 'Text_Attribute_Work'
        db.create_table('editions_text_attribute_work', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text_attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Text_Attribute'])),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Work'])),
        ))
        db.send_create_signal('editions', ['Text_Attribute_Work'])

        # Adding model 'Editor_Edition'
        db.create_table('editions_editor_edition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Editor'])),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Edition'])),
        ))
        db.send_create_signal('editions', ['Editor_Edition'])

        # Adding model 'Bibliographic_Entry_Bib_Category'
        db.create_table('editions_bibliographic_entry_bib_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bibliographic_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Bibliographic_Entry'])),
            ('bib_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Bib_Category'])),
        ))
        db.send_create_signal('editions', ['Bibliographic_Entry_Bib_Category'])

        # Adding model 'Version_Witness'
        db.create_table('editions_version_witness', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Version'])),
            ('witness', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Witness'])),
        ))
        db.send_create_signal('editions', ['Version_Witness'])

        # Adding model 'Witness_Language'
        db.create_table('editions_witness_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('witness', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Witness'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Language'])),
        ))
        db.send_create_signal('editions', ['Witness_Language'])

        # Adding model 'Version_Language'
        db.create_table('editions_version_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Version'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Language'])),
        ))
        db.send_create_signal('editions', ['Version_Language'])

        # Adding model 'Edition_Bibliographic_Entry'
        db.create_table('editions_edition_bibliographic_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('edition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Edition'])),
            ('bibliographic_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['editions.Bibliographic_Entry'])),
            ('page_ranges', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True)),
        ))
        db.send_create_signal('editions', ['Edition_Bibliographic_Entry'])


    def backwards(self, orm):
        # Removing unique constraint on 'Topic', fields ['name']
        db.delete_unique('editions_topic', ['name'])

        # Removing unique constraint on 'Place', fields ['name']
        db.delete_unique('editions_place', ['name'])

        # Removing unique constraint on 'Version_Relationship_Type', fields ['name']
        db.delete_unique('editions_version_relationship_type', ['name'])

        # Removing unique constraint on 'Folio_Side', fields ['name']
        db.delete_unique('editions_folio_side', ['name'])

        # Removing unique constraint on 'Sigla_Provenance', fields ['name']
        db.delete_unique('editions_sigla_provenance', ['name'])

        # Removing unique constraint on 'Archive', fields ['city', 'name']
        db.delete_unique('editions_archive', ['city', 'name'])

        # Removing unique constraint on 'Bib_Category', fields ['name']
        db.delete_unique('editions_bib_category', ['name'])

        # Removing unique constraint on 'Language', fields ['name']
        db.delete_unique('editions_language', ['name'])

        # Removing unique constraint on 'EEL_Edition_Status', fields ['name']
        db.delete_unique('editions_eel_edition_status', ['name'])

        # Removing unique constraint on 'Editor', fields ['abbreviation']
        db.delete_unique('editions_editor', ['abbreviation'])

        # Removing unique constraint on 'Manuscript', fields ['shelf_mark']
        db.delete_unique('editions_manuscript', ['shelf_mark'])

        # Removing unique constraint on 'Folio_Image', fields ['filepath']
        db.delete_unique('editions_folio_image', ['filepath'])

        # Removing unique constraint on 'Work', fields ['name']
        db.delete_unique('editions_work', ['name'])

        # Removing unique constraint on 'Glossary_Term', fields ['term']
        db.delete_unique('editions_glossary_term', ['term'])

        # Removing unique constraint on 'Text_Attribute', fields ['name']
        db.delete_unique('editions_text_attribute', ['name'])

        # Removing unique constraint on 'Version', fields ['standard_abbreviation']
        db.delete_unique('editions_version', ['standard_abbreviation'])

        # Removing unique constraint on 'Person', fields ['name']
        db.delete_unique('editions_person', ['name'])

        # Deleting model 'Person'
        db.delete_table('editions_person')

        # Deleting model 'Version'
        db.delete_table('editions_version')

        # Deleting model 'Text_Attribute'
        db.delete_table('editions_text_attribute')

        # Deleting model 'Glossary_Term'
        db.delete_table('editions_glossary_term')

        # Deleting model 'Work'
        db.delete_table('editions_work')

        # Deleting model 'Commentary'
        db.delete_table('editions_commentary')

        # Deleting model 'Folio_Image'
        db.delete_table('editions_folio_image')

        # Deleting model 'Bibliographic_Entry'
        db.delete_table('editions_bibliographic_entry')

        # Deleting model 'Manuscript'
        db.delete_table('editions_manuscript')

        # Deleting model 'Edition'
        db.delete_table('editions_edition')

        # Deleting model 'Witness_Transcription'
        db.delete_table('editions_witness_transcription')

        # Deleting model 'Witness_Translation'
        db.delete_table('editions_witness_translation')

        # Deleting model 'Edition_Translation'
        db.delete_table('editions_edition_translation')

        # Deleting model 'Witness'
        db.delete_table('editions_witness')

        # Deleting model 'Editor'
        db.delete_table('editions_editor')

        # Deleting model 'EEL_Edition_Status'
        db.delete_table('editions_eel_edition_status')

        # Deleting model 'King'
        db.delete_table('editions_king')

        # Deleting model 'Language'
        db.delete_table('editions_language')

        # Deleting model 'Bib_Category'
        db.delete_table('editions_bib_category')

        # Deleting model 'Archive'
        db.delete_table('editions_archive')

        # Deleting model 'Sigla_Provenance'
        db.delete_table('editions_sigla_provenance')

        # Deleting model 'Folio_Side'
        db.delete_table('editions_folio_side')

        # Deleting model 'Version_Relationship_Type'
        db.delete_table('editions_version_relationship_type')

        # Deleting model 'Version_Relationship'
        db.delete_table('editions_version_relationship')

        # Deleting model 'Place'
        db.delete_table('editions_place')

        # Deleting model 'Topic'
        db.delete_table('editions_topic')

        # Deleting model 'Hyparchetype'
        db.delete_table('editions_hyparchetype')

        # Deleting model 'Resource'
        db.delete_table('editions_resource')

        # Deleting model 'User_Comment'
        db.delete_table('editions_user_comment')

        # Deleting model 'Text_Attribute_Work'
        db.delete_table('editions_text_attribute_work')

        # Deleting model 'Editor_Edition'
        db.delete_table('editions_editor_edition')

        # Deleting model 'Bibliographic_Entry_Bib_Category'
        db.delete_table('editions_bibliographic_entry_bib_category')

        # Deleting model 'Version_Witness'
        db.delete_table('editions_version_witness')

        # Deleting model 'Witness_Language'
        db.delete_table('editions_witness_language')

        # Deleting model 'Version_Language'
        db.delete_table('editions_version_language')

        # Deleting model 'Edition_Bibliographic_Entry'
        db.delete_table('editions_edition_bibliographic_entry')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'editions.archive': {
            'Meta': {'ordering': "['name', 'city']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Archive'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        },
        'editions.bib_category': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name',),)", 'object_name': 'Bib_Category'},
            'bibliographic_entry': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['editions.Bibliographic_Entry']", 'null': 'True', 'through': "orm['editions.Bibliographic_Entry_Bib_Category']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        },
        'editions.bibliographic_entry': {
            'Meta': {'object_name': 'Bibliographic_Entry'},
            'authors': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['editions.Edition']", 'null': 'True', 'through': "orm['editions.Edition_Bibliographic_Entry']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Language']"}),
            'publication_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'styled_reference': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'title_article': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'title_monograph': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'})
        },
        'editions.bibliographic_entry_bib_category': {
            'Meta': {'object_name': 'Bibliographic_Entry_Bib_Category'},
            'bib_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Bib_Category']"}),
            'bibliographic_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Bibliographic_Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'editions.commentary': {
            'Meta': {'object_name': 'Commentary'},
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Edition']"}),
            'elementid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'editions.edition': {
            'Meta': {'object_name': 'Edition'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'date_of_edition': ('cch.fuzzydate.fields.FuzzyDateField', [], {'modifier': 'True', 'null': 'True', 'blank': 'True'}),
            'date_of_edition_mod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_of_edition_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edition_translation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Edition_Translation']", 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['editions.Editor']", 'through': "orm['editions.Editor_Edition']", 'symmetrical': 'False'}),
            'eel_edition_status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.EEL_Edition_Status']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'introduction': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'rendered_apparatus': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'rendered_commentary': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'rendered_edition': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'rendered_translation': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Version']"})
        },
        'editions.edition_bibliographic_entry': {
            'Meta': {'object_name': 'Edition_Bibliographic_Entry'},
            'bibliographic_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Bibliographic_Entry']"}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Edition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_ranges': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'})
        },
        'editions.edition_translation': {
            'Meta': {'object_name': 'Edition_Translation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'})
        },
        'editions.editor': {
            'Meta': {'unique_together': "(('abbreviation',),)", 'object_name': 'Editor'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'})
        },
        'editions.editor_edition': {
            'Meta': {'object_name': 'Editor_Edition'},
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Edition']"}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Editor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'editions.eel_edition_status': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'EEL_Edition_Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.folio_image': {
            'Meta': {'unique_together': "(('filepath',),)", 'object_name': 'Folio_Image'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'batch': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'filename_sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'filepath': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'folio_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'folio_side': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Folio_Side']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_notes': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'manuscript': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Manuscript']"}),
            'page': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        'editions.folio_side': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Folio_Side'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.glossary_term': {
            'Meta': {'unique_together': "(('term',),)", 'object_name': 'Glossary_Term'},
            'description': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.hyparchetype': {
            'Meta': {'object_name': 'Hyparchetype'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Edition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sigla': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'})
        },
        'editions.king': {
            'Meta': {'object_name': 'King', '_ormbases': ['editions.Person']},
            'beginning_regnal_year': ('cch.fuzzydate.fields.FuzzyDateField', [], {'modifier': 'True', 'null': 'True', 'blank': 'True'}),
            'beginning_regnal_year_mod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'beginning_regnal_year_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_regnal_year': ('cch.fuzzydate.fields.FuzzyDateField', [], {'modifier': 'True', 'null': 'True', 'blank': 'True'}),
            'end_regnal_year_mod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'end_regnal_year_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['editions.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        'editions.language': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Language'},
            'color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'version': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['editions.Version']", 'null': 'True', 'through': "orm['editions.Version_Language']", 'blank': 'True'}),
            'witness': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['editions.Witness']", 'null': 'True', 'through': "orm['editions.Witness_Language']", 'blank': 'True'})
        },
        'editions.manuscript': {
            'Meta': {'ordering': "['shelf_mark', 'archive']", 'unique_together': "(('shelf_mark',),)", 'object_name': 'Manuscript'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Archive']"}),
            'checked_folios': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'hide_folio_numbers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hide_from_listings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shelf_mark': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'sigla': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'sigla_provenance': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Sigla_Provenance']"}),
            'single_sheet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'standard_edition': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'editions.person': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.place': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Place'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.resource': {
            'Meta': {'object_name': 'Resource'},
            'caption': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        },
        'editions.sigla_provenance': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Sigla_Provenance'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.text_attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name',),)", 'object_name': 'Text_Attribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.text_attribute_work': {
            'Meta': {'object_name': 'Text_Attribute_Work'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text_attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Text_Attribute']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Work']"})
        },
        'editions.topic': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'})
        },
        'editions.user_comment': {
            'Meta': {'object_name': 'User_Comment'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'division': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'editionid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'editions.version': {
            'Meta': {'ordering': "['standard_abbreviation']", 'unique_together': "(('standard_abbreviation',),)", 'object_name': 'Version'},
            'date': ('cch.fuzzydate.fields.FuzzyDateField', [], {'modifier': 'True', 'null': 'True', 'blank': 'True'}),
            'date_mod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'graph': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'print_editions': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'standard_abbreviation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'synopsis': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'synopsis_manuscripts': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Work']"})
        },
        'editions.version_language': {
            'Meta': {'object_name': 'Version_Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Language']"}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Version']"})
        },
        'editions.version_relationship': {
            'Meta': {'object_name': 'Version_Relationship'},
            'description': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'version_relationship_source'", 'to': "orm['editions.Version']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'version_relationship_target'", 'to': "orm['editions.Version']"}),
            'version_relationship_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Version_Relationship_Type']"})
        },
        'editions.version_relationship_type': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Version_Relationship_Type'},
            'description': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'})
        },
        'editions.version_witness': {
            'Meta': {'object_name': 'Version_Witness'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Version']"}),
            'witness': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Witness']"})
        },
        'editions.witness': {
            'Meta': {'object_name': 'Witness'},
            'description': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'hide_from_listings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manuscript': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Manuscript']"}),
            'medieval_translation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'range_end': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'range_start': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'rendered_facsimiles': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['editions.Version']", 'through': "orm['editions.Version_Witness']", 'symmetrical': 'False'}),
            'witness_transcription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Witness_Transcription']", 'null': 'True', 'blank': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['editions.Work']"})
        },
        'editions.witness_language': {
            'Meta': {'object_name': 'Witness_Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Language']"}),
            'witness': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Witness']"})
        },
        'editions.witness_transcription': {
            'Meta': {'object_name': 'Witness_Transcription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rendered_text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'witness_translation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.Witness_Translation']", 'null': 'True', 'blank': 'True'})
        },
        'editions.witness_translation': {
            'Meta': {'object_name': 'Witness_Translation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rendered_text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'}),
            'text': ('django.db.models.fields.XMLField', [], {'default': "''", 'blank': 'True'})
        },
        'editions.work': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name',),)", 'object_name': 'Work'},
            'date': ('cch.fuzzydate.fields.FuzzyDateField', [], {'modifier': 'True', 'null': 'True', 'blank': 'True'}),
            'date_mod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'king': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['editions.King']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'text_attribute': ('django.db.models.fields.related.ManyToManyField', [], {'default': '1', 'to': "orm['editions.Text_Attribute']", 'through': "orm['editions.Text_Attribute_Work']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['editions']