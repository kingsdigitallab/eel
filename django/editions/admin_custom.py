# auto generated from an XMI file
# this file can be edit,
# make sure it is renamed into "admin_custom.py" (without the underscore
# at the beginning)
import re
from django.utils.safestring import mark_safe
from django.contrib import admin
from editions.models import (
    Edition,
    Editor_Edition,
    Folio_Image,
    Hyparchetype,
    Text_Attribute_Work,
    Edition_Translation,
    User_Comment,
    Version,
    Version_Language,
    Version_Witness,
    Witness,
    Witness_Language,
)
from editions.admin_generic import (
    Bibliographic_Entry_Bib_CategoryInline,
    Editor_EditionInline,
    Version_LanguageInline,
    Witness_LanguageInline,
    ArchiveAdmin,
    Bib_CategoryAdmin,
    Bibliographic_EntryAdmin,
    CommentaryAdmin,
    Edition_TranslationAdmin,
    EditionAdmin,
    EditorAdmin,
    EEL_Edition_StatusAdmin,
    Folio_ImageAdmin,
    Glossary_TermAdmin,
    HyparchetypeAdmin,
    KingAdmin,
    LanguageAdmin,
    ManuscriptAdmin,
    ResourceAdmin,
    Text_AttributeAdmin,
    User_CommentAdmin,
    Version_RelationshipAdmin,
    VersionAdmin,
    Witness_TranscriptionAdmin,
    Witness_TranslationAdmin,
    WitnessAdmin,
    WorkAdmin)

from cch import aop
from django import forms
from cch.admin import utils as utils
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ValidationError
from cch.admin.utils import LabelWidget
from editions.models_generic import Folio_Side

# -----------------------
#   FORMS
# -----------------------


class User_CommentForm(forms.ModelForm):

    class Meta:
        model = User_Comment

    user = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    text = forms.CharField(widget=utils.RawHtmlWidget, required=False,)

    def __init__(self, *args, **kwargs):
        super(User_CommentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            web_user = instance.get_web_user()
            text = instance.get_text()
            self.fields['user'].initial = ur'<a href="%s">%s</a>' % (
                utils.get_admin_webpath_from_object(web_user, True), web_user.user)
            self.fields['text'].initial = ur'<a href="%s">%s</a>' % (
                utils.get_admin_webpath_from_object(text, True), text)


class EditionForm(forms.ModelForm):

    class Meta:
        model = Edition

    download = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    text_viewer = forms.CharField(
        widget=utils.RawHtmlWidget,
        required=False,
        help_text='''NOTE THAT THERE MIGHT BE A FEW HOURS DELAY BETWEEN LAST
        EDIT AND THIS PREVIEW. Use internal preview tool for more immediate
        or frequent review.'''
    )

    edition = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    translation = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    witnesses = forms.CharField(widget=utils.RawHtmlWidget, required=False,)

    def __init__(self, *args, **kwargs):
        super(EditionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            self.fields['edition'].initial = ur'<a href="text">Edit the text of this edition.</a>'
            self.fields['translation'].initial = ur'<a href="translation">Edit the translation of this edition.</a>'
            self.fields['witnesses'].initial = self.getWitnessLinks(instance)
            self.fields['download'].initial = ur'<a href="download">Download the edition, translation, witnesses and introduction</a>'
            # TODO: don't hard-code url here
            text_viewer_url = ur'/laws/texts/%s/view/' % instance.version.slug
            self.fields['text_viewer'].initial = ur'<a href="%s">Preview in the Text Viewer</a>' % text_viewer_url

    def getWitnessLinks(self, edition):
        ret = ''
        # get the list of all the witnesses used by the version this edition is
        # based on
        for witness in Witness.objects.filter(
                version=edition.version).order_by('manuscript__sigla'):
            witness_link = u'''<td>%s</td>''' % witness.__unicode__()

            if not witness.manuscript.hide_from_listings:
                transcid = 0
                translid = 0
                transc = witness.witness_transcription
                if transc:
                    transcid = transc.id
                    transl = transc.witness_translation
                    if transl:
                        translid = transl.id
                label = 'create transcription'

                if transcid:
                    label = 'edit transcription'
                witness_link = witness_link + \
                    u'''<td><a href="../../witness/%s/transcription">%s</a></td>''' % (
                        witness.id, label)

                label = 'create translation'
                if translid:
                    label = 'edit translation'
                witness_link = witness_link + \
                    u'''<td><a href="../../witness/%s/translation">%s</a></td>''' % (
                        witness.id, label)
            else:
                witness_link = witness_link + u'<td>(late manuscript)</td>'

            ret = ret + '<tr>%s</tr>' % witness_link

        if len(ret):
            ret = '<table>%s</table>' % ret
        else:
            ret = 'No witness found for this edition.'

        return ret

    def clean_introduction(self):
        ret = get_clean_text(self.cleaned_data['introduction'])
        return ret


class Bibliographic_EntryForm(forms.ModelForm):

    def clean_styled_reference(self):
        # remove blank lines
        text = self.cleaned_data['styled_reference']

        # remove chain of spaces
        text = re.sub('(?iu)\s+', ' ', text)
        # remove empty paragraphs
        text = re.sub('(?iu)<p>\s*</p>', '', text).strip()

        # let's shout if the BE contains more than one paragraph
        matches = re.findall(r'(?i)</p>', text)
        if matches is not None and len(matches) > 1:
            raise ValidationError(
                mark_safe("The Bibliographic Entry should stand on a single line."))
        return text


class VersionForm(forms.ModelForm):
    # AC # 48
    # We override the slug field to have a LabelWidget AND required=False
    # slug in the model/DB is still required but because it's populated on save
    # we don't have a value in advance for new Version
    slug = forms.SlugField(
        max_length=250,
        required=False,
        widget=LabelWidget()
    )

    class Meta:
        model = Version


class Folio_ImageForm(forms.ModelForm):

    view_image = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    # TODO: this and the related clean_ method should be generalised (also used in other places)
    #internal_notes = forms.CharField(widget=forms.Textarea, required = False , help_text=Folio_Image._meta.get_field_by_name('internal_notes')[0].help_text)

    class Meta:
        model = Folio_Image

    def __init__(self, *args, **kwargs):
        super(Folio_ImageForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        # make those fields read only
        self.fields['batch'].widget = LabelWidget()
        self.fields['path'].widget = LabelWidget()
        self.fields['filename'].widget = LabelWidget()
        self.fields['filepath'].widget = LabelWidget()
        self.fields['internal_notes'].widget = forms.Textarea()
        if instance and instance.id:
            self.fields['view_image'].initial = Folio_ImageForm.image_link(
                instance)

    @staticmethod
    def image_link(obj):
        ret = ''
        if obj is not None and obj.id > 0:
            ret = '<a href="%s" class="img-prv">view</a>' % obj.get_image_url_full()
        return mark_safe(ret)

    def internal_notes(self):
        # we must validate the length here as the field is rendered with a
        # textarea (no limit)
        field_name = 'internal_notes'
        field_def = self.instance._meta.get_field_by_name(field_name)[0]
        if len(self.cleaned_data[field_name]) > field_def.max_length:
            raise ValidationError(
                'This value is longer than %d characters.' %
                field_def.max_length)
        return self.cleaned_data[field_name]

#


class HyparchetypeForm(forms.ModelForm):

    class Meta:
        model = Hyparchetype

    def __init__(self, *args, **kwargs):
        super(HyparchetypeForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea()

    def description(self):
        # we must validate the length here as the field is rendered with a
        # textarea (no limit)
        field_name = 'description'
        field_def = self.instance._meta.get_field_by_name(field_name)[0]
        if len(self.cleaned_data[field_name]) > field_def.max_length:
            raise ValidationError(
                'This value is longer than %d characters.' %
                field_def.max_length)
        return self.cleaned_data[field_name]


#-----------------------
#		INLINES
#-----------------------

#
class Bibliographic_Entry_Bib_CategoryInline(
        Bibliographic_Entry_Bib_CategoryInline):
    extra = 3
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'

#


class Version_LanguageInline(Version_LanguageInline):
    verbose_name = "Language"
    verbose_name_plural = "Languages"
    model = Version_Language
    extra = 3

#


class HyparchetypeInline(admin.TabularInline):
    model = Hyparchetype
    form = HyparchetypeForm
    extra = 2

#


class VersionInline(admin.TabularInline):
    #verbose_name = "Version"
    #verbose_name_plural = "Versions"
    model = Version
    extra = 2

#	fieldsets = (
#		('', {'fields' : ('name', )}),
#	)

#


class Text_Attribute_WorkInline(admin.TabularInline):
    verbose_name = "Text Attribute"
    verbose_name_plural = "Text Attributes"
    model = Text_Attribute_Work
    extra = 3

#


class Work_WitnessInline(admin.StackedInline):
    model = Witness
    extra = 3

    fieldsets = (
        ('', {'fields': ('manuscript', 'range_start', 'range_end')}),
    )

#


class Editor_EditionInline(Editor_EditionInline):
    verbose_name = "Editor"
    verbose_name_plural = "Editors"
    model = Editor_Edition
    extra = 3


class Version_WitnessInline(admin.TabularInline):
    verbose_name = "Version - Witness"
    verbose_name_plural = "Versions - Witnesses"
    model = Version_Witness
    extra = 3

#


class Witness_LanguageInline(Witness_LanguageInline):
    verbose_name = "Language"
    verbose_name_plural = "Languages"
    model = Witness_Language
    extra = 3

#-----------------------
#		CORE TABLES
#-----------------------

#


class WorkAdmin(WorkAdmin):
    fieldsets = (
        ('', {'fields': ('name', 'king', 'date')}),
    )

    list_display = ('id', 'name', 'king')
    list_display_links = list_display
    list_filter = ['king', 'text_attribute']

    # Version_Inline, Work_WitnessInline
    inlines = [Text_Attribute_WorkInline, ]

#


class WitnessAdmin(WitnessAdmin):
    fieldsets = (
        ('Work', {'fields': ('work', )}),
        ('Location', {'fields': ('manuscript',
                                 'range_start', 'range_end', 'page')}),
        # 'medieval_translation'
        ('Description', {'fields': ('description', )}),
    )

    list_display = ('id', 'work', 'manuscript', 'range_start', 'range_end', )
    list_display_links = list_display
    #list_filter = ('eel_edition_status',)

    #ordering = ('authors', 'publication_date', 'title',)
    ordering = ('work',)

    inlines = (Witness_LanguageInline, Version_WitnessInline)

    search_fields = ('id', 'range_start', 'range_end')

#


class EditionAdmin(EditionAdmin):
    fieldsets = (
        ('', {'fields': ('abbreviation', 'version',
                         'date_of_edition', 'eel_edition_status',
                         'text_viewer', 'download'
                         )}),
        ('Encoded texts', {'fields': ('edition', 'translation', 'witnesses')}),
        ('Introduction', {'fields': ('introduction',)}),
        ('Further information', {'fields': ('internal_notes',)}),
    )

    form = EditionForm

    list_display = ('id', 'abbreviation', 'eel_edition_status', 'version')
    list_display_links = list_display
    list_filter = ('eel_edition_status',)

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('abbreviation',)

    inlines = (Editor_EditionInline, HyparchetypeInline)

    search_fields = ('id', 'abbreviation')

#


class ManuscriptAdmin(ManuscriptAdmin):
    fieldsets = (
        ('Sigla', {'fields': ('sigla', 'sigla_provenance',)}),
        ('Archive', {'fields': ('archive', 'shelf_mark',)}),
        ('Others', {'fields': ('description', 'hide_from_listings',
                               'checked_folios', 'single_sheet', 'standard_edition')}),
    )

    list_display = ('id', 'sigla', 'shelf_mark', 'archive', 'single_sheet')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('archive', 'shelf_mark',)

    #inlines = (Bibliographic_Entry_Bib_CategoryInline, )

    search_fields = ['id', 'shelf_mark', 'sigla']

    list_filter = [
        'single_sheet',
        'hide_from_listings',
        'checked_folios',
        'sigla_provenance',
        'archive']

#


class VersionAdmin(VersionAdmin):
    fieldsets = (
        ('Info', {'fields': ('standard_abbreviation',
                             'slug', 'name', 'work', 'date')}),
        ('Synopsis',
         {'fields': ('synopsis',
                     'synopsis_manuscripts',
                     'print_editions')}),
    )

    form = VersionForm

    # disabled as we don't want ppl to use this by mistake
    #actions = ['set_versions_work', 'clean_names']

    list_display = ('id', 'standard_abbreviation', 'slug', 'version_name')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('standard_abbreviation',)

    inlines = (Version_LanguageInline, Version_WitnessInline, )

    search_fields = ['id', 'standard_abbreviation']

    #list_filter = ['language']

    def clean_names(self, request, queryset):
        for version in Version.objects.all():
            if version.name == version.work.name:
                version.name = ''
            version.save()

    def set_versions_work(self, request, queryset):
        main_work = None
        # find the work with the lowest id
        for version in queryset:
            if version.work is not None and (
                    main_work is None or version.work.id < main_work.id):
                main_work = version.work
        # remove all other works and link all the version to the main work
        for version in queryset:
            if version.work != main_work:
                version.work.delete()
                version.work = main_work
                version.save()
        self.message_user(
            request,
            "%s versions were successfully grouped under the same law/work." %
            queryset.count())
    set_versions_work.short_description = 'Group by law'

#-----------------------
#		OTHER TABLES
#-----------------------


class Version_RelationshipAdmin(Version_RelationshipAdmin):
    fieldsets = (
        ('', {'fields': ('version_relationship_type',
                         'source', 'target', 'description')}),
    )

    # disabled as we don't want ppl to use this by mistake
    #actions = ['set_versions_work', 'clean_names']

    list_display = ('id', 'version_relationship_type', 'source', 'target')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('source',)

    list_filter = ['version_relationship_type']

    #inlines = (Version_LanguageInline, Version_WitnessInline, )

    search_fields = ['id']


class ResourceAdmin(ResourceAdmin):
    fieldsets = (
        ('', {'fields': ('title', 'file', 'caption')}),
    )

    list_display = ('id', 'title')
    list_display_links = list_display


class Bibliographic_EntryAdmin(Bibliographic_EntryAdmin):

    form = Bibliographic_EntryForm

    fieldsets = (
        ('Reference', {'fields': ('styled_reference', )}),
        ('Others', {'fields': ('language', )}),
    )

    list_display = (
        'id',
        'authors',
        'publication_date',
        'title_monograph',
        'title_article')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('styled_reference',)

    inlines = (Bibliographic_Entry_Bib_CategoryInline, )

    search_fields = ['styled_reference']

    list_filter = ['language']

    def render_change_form(self, request, context, *args, **kwargs):
        """Custom wysiwyg on this page"""
        context.update({'wysiwyg_fields_custom': 'id_styled_reference',
                        'wysiwyg_fields_custom_buttons1': 'italic,CCHauthor,CCHeditor,CCHtitlemonograph,CCHtitlearticle,CCHdate,CCHunmark,separator,undo,redo,separator,code',
                        'wysiwyg_fields_noref': 'id_styled_reference'})

        superclass = super(Bibliographic_EntryAdmin, self)
        return superclass.render_change_form(request, context, *args, **kwargs)

#


class Text_AttributeAdmin(Text_AttributeAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display

#


class Glossary_TermAdmin(Glossary_TermAdmin):
    list_display = ('id', 'term')
    list_display_links = list_display

    ordering = ('term', )

#


class CommentaryAdmin(CommentaryAdmin):
    pass

#


class Folio_ImageAdmin(Folio_ImageAdmin):

    form = Folio_ImageForm

    fieldsets = (
        ('Image file', {'fields': ('filename',
                                   'view_image', 'batch', 'path', 'filepath')}),
        ('Manuscript', {'fields': ('manuscript', 'folio_number',
                                   'folio_side', 'page', 'display_order', )}),
        ('Archival', {'fields': ('archived', )}),
        ('Notes', {'fields': ('internal_notes', )}),
    )

    actions = ['bulk_natural_sorting', 'bulk_editing']

    list_display = (
        'id',
        'batch',
        'path',
        'filename',
        'folio_number',
        'page',
        'image_link',
        'archived')
    #list_editable = ('folio_number', 'page', )
    #list_display_links = ('id', 'batch', 'path', 'filename', )
    list_display_links = (
        'id',
        'batch',
        'path',
        'filename',
        'folio_number',
        'page',
        'archived')

    list_per_page = 300

    ordering = ('batch', 'path', 'filename')
    special_ordering = {
        'batch': (
            'batch', 'path', 'filename_sort_order'
        ),
        'path': (
            'path', 'filename_sort_order'
        )
    }

    #inlines = (Bibliographic_Entry_Bib_CategoryInline, )

    search_fields = ['id', 'filepath', 'internal_notes', ]

    list_filter = ['archived', 'batch', 'manuscript', 'path', ]

    def get_changelist(self, request, **kwargs):
        return utils.SpecialOrderingChangeList

    def image_link(self, obj):
        return self.form.image_link(obj)
    image_link.short_description = 'View'
    image_link.allow_tags = True

    def bulk_editing(self, request, queryset):
        from django.http import HttpResponseRedirect
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("bulk_edit/?ids=%s" % (",".join(selected)))
    bulk_editing.short_description = 'Bulk edit'

    def bulk_natural_sorting(self, request, a_queryset):
        count = Folio_Image.objects.bulkNaturalFileNameSortOrder()
        Folio_Image.objects.bulkNaturalDisplayOrderSorting()
        self.message_user(request, r"%s sort order reset." % count)
    bulk_natural_sorting.short_description = 'Reset natural sort order'

    def bulk_set_folio_side(self, request, queryset):
        counts = {'r': 0, 'v': 0, 'u': 0}
        unspecified = Folio_Side.objects.get(id=1)
        recto = Folio_Side.objects.get(id=3)
        verso = Folio_Side.objects.get(id=4)
        for folio in queryset:
            if re.search('(?i)[^a-z]r$', folio.filename):
                folio.folio_side = recto
                counts['r'] = counts['r'] + 1
            elif re.search('(?i)[^a-z]v$', folio.filename):
                folio.folio_side = verso
                counts['v'] = counts['v'] + 1
            else:
                folio.folio_side = unspecified
                counts['u'] = counts['u'] + 1
            folio.save()
        self.message_user(
            request, r"%s images: %s recto, %s verso, %s unspecified." %
            (queryset.count(), counts['r'], counts['v'], counts['u']))
    bulk_set_folio_side.short_description = 'Set folio side'

#


class Witness_TranscriptionAdmin(Witness_TranscriptionAdmin):
    fieldsets = (
        ('Witness', {'fields': ('text',)}),
    )

    list_display = ('id', 'getWitness')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    #ordering = ('getWitness',)

    #inlines = (Editor_EditionInline, )

    search_fields = ('id',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

#


class Witness_TranslationAdmin(Witness_TranslationAdmin):
    list_display = ('id', '__unicode__')
    list_display_links = list_display

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

#


class Edition_TranslationForm(forms.ModelForm):

    class Meta:
        model = Edition_Translation

    edition = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    translation = forms.CharField(widget=utils.RawHtmlWidget, required=False,)
    size = forms.CharField(widget=utils.RawHtmlWidget, required=False,)

    def __init__(self, *args, **kwargs):
        super(Edition_TranslationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.id:
            edition = instance.get_edition()
            if edition:
                base_url = '/admin/editions/edition/%s' % edition.pk
                self.fields['edition'].initial = ur'<a href="%s/">See the edition record.</a>' % base_url
                self.fields['translation'].initial = ur'<a href="%s/translation">Edit the translation of this edition.</a>' % base_url
            else:
                self.fields['edition'].initial = ur'ERROR: this translation is not linked to an edition'
                self.fields['translation'].initial = ur'ERROR: this translation is not linked to an edition'
            self.fields['size'].initial = ur'%s Bytes' % len(instance.text)


class Edition_TranslationAdmin(Edition_TranslationAdmin):
    list_display = ('id', '__unicode__')
    list_display_links = list_display
    ordering = ('id',)

    form = Edition_TranslationForm

    fieldsets = (
        ('Links', {'fields': ('edition', 'translation', 'size')}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

#


class EditorAdmin(EditorAdmin):

    fieldsets = (
        ('Name', {'fields': ('abbreviation', 'last_name', 'first_name')}),
    )

    list_display = ('id', 'abbreviation', 'last_name', 'first_name')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('last_name',)

    inlines = (Editor_EditionInline, )

    search_fields = list_display

#


class EEL_Edition_StatusAdmin(EEL_Edition_StatusAdmin):
    pass

#


class KingAdmin(KingAdmin):
    pass

#


class LanguageAdmin(LanguageAdmin):
    pass

    inlines = []

#


class Bib_CategoryAdmin(Bib_CategoryAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display

    inlines = []

#


class HyparchetypeAdmin(HyparchetypeAdmin):

    form = HyparchetypeForm

    fieldsets = (
        ('Information', {'fields': ('sigla', 'edition', 'description')}),
    )
    list_display = ('id', 'edition', 'sigla')
    list_display_links = list_display

    ordering = ('edition', 'sigla',)

    search_fields = ['id', 'sigla']

    inlines = []

#


class ArchiveAdmin(ArchiveAdmin):
    fieldsets = (
        ('Archive', {'fields': ('name', 'city', 'country')}),
    )

    list_display = ('id', 'name', 'city', 'country')
    list_display_links = list_display

    # ordering = ('authors', 'publication_date', 'title',)
    ordering = ('city', 'name',)

    #inlines = (Bibliographic_Entry_Bib_CategoryInline, )

    search_fields = ['id', 'name', 'city', 'country']

    list_filter = ['country', 'city', ]


class User_CommentAdmin(User_CommentAdmin):

    form = User_CommentForm

    fieldsets = (
        ('Comment', {'fields': ('comment', 'private',
                                'archived', 'timestamp', 'user', 'text', 'division')}),
    )

    list_display = (
        'id',
        'timestamp',
        'user_name',
        'text_name',
        'comment_first_words',
        'archived',
        'private',
    )
    list_display_links = list_display

    ordering = ('-id',)

    search_fields = ['id', 'userid', 'comment']
    list_filter = ['private', 'archived', ]

#-----------------------
#    HELPERS FUNCTIONS
#-----------------------


def add_wysiwyg_fields_to_context(
        model_admin, request, context, *args, **kwargs):
    '''add a variable to the context which value is a comma separated list of
    the html id of the XML fields in the model'''
    wysiwyg_fields = []
    from django.db.models.fields import XMLField
    for field in model_admin.model._meta.fields:
        if (isinstance(field, XMLField)):
            wysiwyg_fields.append('id_' + field.get_attname())
    context.update({'wysiwyg_fields': ','.join(wysiwyg_fields)})


aop.execute_before(
    admin.ModelAdmin,
    'render_change_form',
    add_wysiwyg_fields_to_context)


# Globally disable delete selected
admin.site.disable_action('delete_selected')

#-----------------------
#    ENABLE MULTI-FIELD SORTING IN THE LIST VIEWS
#-----------------------

##


def apply_special_ordering(self, queryset):
        # https://github.com/benatkin/tuneage/blob/master/tunes/admin.py
        # http://python-web.blogspot.com/
        # Adapted for Django 1.1
    order_by, order_type = self.get_ordering()
    special_ordering = getattr(self.model_admin, 'special_ordering', None)
    if special_ordering and order_type and order_by and order_by in special_ordering:
        try:
            ordering = special_ordering[order_by]
            sign = ''
            if order_type == 'desc':
                sign = '-'
            ordering = [sign + field for field in ordering]
            queryset = queryset.order_by(*ordering)
        except Exception:
            pass
    return queryset


def get_query_set(self):
    queryset = self.get_query_set_old()
    queryset = self.apply_special_ordering(queryset)
    return queryset


ChangeList.apply_special_ordering = apply_special_ordering
ChangeList.get_query_set_old = ChangeList.get_query_set
ChangeList.get_query_set = get_query_set


def get_clean_text_one_pass(txt):
    ''' Returns the xml document as a string without superfluous divs.
        * <div> containing only 1 <p> are removed
        * <div> containing only text are converted into <p>
        * text node consisting of a single blank are removed
            * otherwise the two previous rules would not work
    '''
    from lxml import etree, html

    xslt_root = etree.XML('''<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:template match="div[not(@*)][count(p) = 1][count(node()) = 1]">
                <xsl:apply-templates select="node()"/>
            </xsl:template>
            <xsl:template match="div[not(@*)][not(*)]">
                <p>
                    <xsl:apply-templates select="node()"/>
                </p>
            </xsl:template>
            <xsl:template match="text()[. = ' ']"></xsl:template>
            <xsl:template match="node()">
                <xsl:copy>
                    <xsl:apply-templates select="node()|@*"/>
                </xsl:copy>
            </xsl:template>
            <xsl:template match="@*">
                <xsl:copy>
                </xsl:copy>
            </xsl:template>
        </xsl:stylesheet>
    ''')
    xslt = etree.XSLT(xslt_root)
    # Tragically, the supplied txt may not be a valid XML (or
    # HTML) document, having multiple root elements. Therefore
    # append one, and then (deep sigh) remove it via regexp after
    # serialisation. This is clearly wrong, and well-formed XML
    # should be created and saved always, without exception.
    root = html.fragment_fromstring(txt, create_parent='mydoc')
    result = xslt(root)
    dst = etree.tostring(result.getroot(), xml_declaration=False,
                         encoding=unicode)
    dst = re.sub('</?mydoc/?>', '', dst)
    ret = dst.strip()
    return ret


def get_clean_text(txt):
    txt = re.sub(ur'(?u)\s+', ' ', txt)
    ret = get_clean_text_one_pass(txt)
    if len(ret) < len(txt):
        ret = get_clean_text_one_pass(ret)
    return ret


# User Change List
from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display = (
    'id',
    'email',
    'first_name',
    'last_name',
    'is_active',
    'date_joined',
    'is_staff'
)
