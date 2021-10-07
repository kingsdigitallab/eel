from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.admin.views.main import ChangeList


class SpecialOrderingChangeList(ChangeList):
    '''
    https://djangosnippets.org/snippets/2110/
    The new changelist supports clicking on a column header to order by that column,
    like iTunes. Unlike iTunes, which sorts by track number if you click the Artist
    or Album column header, it can only order by the column clicked on. By adding a
    property to my ModelAdmin, and subclassing ChangeList, I was able to make it
    also sort by track number when sorting by Artist or Album.

    Usage:

    class XAdmin(admin.ModelAdmin):
        special_ordering = {'artist': ('artist', 'album', 'track'),
            'album': ('album', 'track')}

        def get_changelist(self, request, **kwargs):
            return SpecialOrderingChangeList
    '''

    def apply_special_ordering(self, queryset):
        order_type, order_by = [
            self.params.get(
                param, None) for param in (
                'ot', 'o')]
        special_ordering = self.model_admin.special_ordering
        if special_ordering and order_type and order_by:
            try:
                order_field = self.list_display[int(order_by)]
                ordering = special_ordering[order_field]
                if order_type == 'desc':
                    ordering = ['-' + field for field in ordering]
                queryset = queryset.order_by(*ordering)
            except IndexError:
                return queryset
            except KeyError:
                return queryset
        return queryset

    def get_query_set(self):
        queryset = super(SpecialOrderingChangeList, self).get_query_set()
        queryset = self.apply_special_ordering(queryset)
        return queryset


def get_admin_webpath_from_object(obj, absolute=False):
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(obj)
    ret = ''
    if absolute:
        ret = '/admin/'
    ret += '%s/%s/%s/' % (content_type.app_label, content_type.model, obj.id)
    return ret


class LabelWidget(TextInput):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    input_type = 'label'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        return mark_safe(
            u'%s <input type="hidden" name="%s" value="%s"/>' % (value, name, value))


class RawHtmlWidget(TextInput):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    input_type = 'raw_html'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        return mark_safe(u'%s' % value)


def newGFKFormClass(model, fk_fields):
    ''' Returns a new class that extends from forms.ModelForm and contains additional fields
            used to describe or link to the objects pointed to by the GenericForeignKey in the model.
        model_name: the name of the model class this form refers to
        fk_fields: a dictionary of field information. The key is the name of the new field in the form.
                    The value if the identifier of the ForeignKeyField in the model class.

        Example usage:
            In your ModelAdmin:
            form = newGFKFormClass(CommentSection, {'commented_record': 'content_object'})

            fieldsets = (
                        [...]'commented_record'[...]
                        }
    '''
    if model is None or fk_fields is None:
        raise Exception('Invalid argument.')
    from new import classobj

    def form_init(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        for field_name in self.fk_fields:
            desc = ''
            if self.instance is not None:
                foreign_object = getattr(
                    self.instance, fk_fields[field_name], None)
                if foreign_object is None:
                    desc = '<span id="id_%s">No record</span>' % (field_name)
                else:
                    desc = '<a id="id_%s" href="../../../%s">%s (%s)</a>' % (field_name, get_admin_webpath_from_object(
                        foreign_object), foreign_object, foreign_object.__class__.__name__)
            self.fields[field_name].initial = desc

    adict = {}
    for field_name in fk_fields:
        model_gfk = getattr(model, fk_fields[field_name], None)
        model_gfk_ct = getattr(model, model_gfk.ct_field, None)
        help_text = getattr(model_gfk_ct.field, 'help_text', '')
        adict[field_name] = forms.CharField(
            required=False, widget=RawHtmlWidget, help_text=help_text)
    adict['Meta'] = classobj('Meta', (), {'model': model})
    # TODO: generate unique identifier for the new class
    ret = classobj(model.__class__.__name__ +
                   'Form', (forms.ModelForm,), adict)
    ret.__init__ = form_init
    ret.fk_fields = fk_fields
    return ret
