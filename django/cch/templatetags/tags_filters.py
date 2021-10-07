# -*- coding: utf-8 -*-
# $Id: tags_filters.py 655 2011-07-12 13:37:45Z gnoel $

from django import template

import re

register = template.Library()


@register.simple_tag
def render_filter(filter, template_name=None):
    from django.template import Context
    if template_name is None:
        template_name = filter.input_type

    # use the template if it exists
    atemplate = template.loader.get_template(
        'cch_filters/' + template_name + '.html')
    ret = atemplate.render(Context({'filter': filter}))
    return ret


@register.simple_tag
def filter_interface(filter, selected_element='li', selected_class=None,
                     bold_items=False, disabled_class=None, link_selected=False):
    ret = u''

#    # use the template if it exists
#    try:
#        ret = render_filter(filter, filter.input_type)
#        return ret
#    except template.TemplateDoesNotExist:
#        print 'ot found'
#        pass

    if filter.input_type == 'box1core':
        ret = ''
        for option in filter.options:
            ret += '<option value="%s"' % option.valname
            if option.selected():
                ret += 'selected="selected"'
            ret += '>%s</option>' % option.label

        ret = u'''<select id="%sid" name="%s">%s</select>''' % (
            filter.varname, filter.varname, ret)
    if filter.input_type == 'box1':
        ret = ''
        for option in filter.options:
            ret += '<option value="%s"' % option.valname
            if option.selected():
                ret += 'selected="selected"'
            ret += '>%s</option>' % option.label

        ret = u'''
                <li>
                    <label for="%sid">%s</label>
                    <select id="%sid" name="%s">%s</select>
                </li>''' % (filter.varname, filter.label, filter.varname, filter.varname, ret)
    if filter.input_type == 'box1old':
        ret = ''
        for option in filter.options:
            ret += '<option value="%s"' % option.valname
            if option.selected():
                ret += 'selected="selected"'
            ret += '>%s</option>' % option.label
        ret = u'''<dt>%s:</dt> <dd><select name="%s">%s</select></dd>''' % (
            filter.label, ret, filter.varname)
    if filter.input_type == 'link-list':
        for option in filter.options:
            ret += '<li'
            if option.selected():
                ret += ' class="s1" '
            ret += u'><a title="%s" class="t1" href="%s">%s</a></li>' % (
                option.label, option.href(), option.label)

        hi = '<input type="hidden" name="%s" value="%s" />' % (
            filter.varname, filter.get_value())

        ret = '<h3>%s</h3><ul>%s </ul> %s' % (filter.label, ret, hi)

    if filter.input_type == 'link':
        for option in filter.options:
            ret += '<dd'
            if option.selected():
                ret += ' class="s1" '
            ret += u'><a title="%s" class="t1" href="%s">%s</a><br/></dd>' % (
                option.label, option.href(), option.label)

        hi = '<input type="hidden" name="%s" value="%s" />' % (
            filter.varname, filter.get_value())

        ret = '<dt>%s %s </dt> %s' % (filter.label, hi, ret)

    if filter.input_type == 'checkbox':
        for option in filter.options:
            selected = ''
            if option.selected():
                selected = ' checked="checked" '
            ret += '''<li>
                          <input id="%sid" type="checkbox" name="%s" value="%s" %s />
                          <label for="%sid">%s</label>
                        </li>''' % (option.valname, filter.varname, option.valname, selected, option.valname, option.label)

        ret = '<li><label for="%s">%s</label><fieldset id="%s"><ol>%s</ol></fieldset></li>' % (
            filter.varname, filter.label, filter.varname, ret)
    if filter.input_type == 'tab':
        # class="s5" is for disabled tabs
        i = 0
        for option in filter.options:
            hidden_input = ''
            if i == 0:
                hidden_input = '<input type="hidden" name="%s" value="%s" />' % (
                    filter.varname, filter.get_value())
            selected = ''
            if option.selected():
                selected = ' class="s1" '
                if selected_class is not None:
                    selected = 'class="%s" ' % selected_class
            item = option.label
            if bold_items:
                item = u'<b>%s</b>' % item
            if selected_element == 'li':
                ret += '<li %s>%s<a href="%s">%s</a></li>' % (
                    selected, hidden_input, option.href(), item)
            else:
                ret += '<li>%s<a %s href="%s">%s</a></li>' % (
                    hidden_input, selected, option.href(), item)
            i += 1
    if filter.input_type == 'column':
        # class="s5" is for disabled tabs
        i = 0
        for option in filter.options:
            hidden_input = ''
            if i == 0:
                hidden_input = '<input type="hidden" name="%s" value="%s" />' % (
                    filter.varname, filter.get_value())
            selected = ''
            if option.selected():
                selected = 'class="s8 m0"'
                if filter.is_ascending():
                    selected = 'class="s8 m1"'
            ret += u'<th %s>%s<a href="%s" title="Sort this data by %s">%s</a></th>' % (
                selected, hidden_input, option.href(), option.label, option.label)
            i += 1
    if filter.input_type == 'page':
        # class="s5" is for disabled tabs
        ret += get_page_link(filter, 0, '<< First', True)
        ret += get_page_link(filter,
                             filter.get_previous_index(),
                             '< Previous',
                             True)
        for option in filter.options:
            ret += get_page_link(filter, int(option.valname), option.label)
        ret += get_page_link(filter, filter.get_next_index(), 'Next >', True)
        ret += get_page_link(filter, filter.get_last_index(), 'Last >>', True)
    if filter.input_type == 'az':
        # class="s5" is for disabled tabs
        filter_hidden_input(filter)
        for option in filter.options:
            ret += get_link_from_option(option,
                                        selected_class,
                                        disabled_class,
                                        link_selected)

    return ret


@register.simple_tag
def filter_hidden_input(filter):
    return '<input type="hidden" name="%s" value="%s" />' % (
        filter.varname, filter.get_value())


def get_link_from_option(option, selected_class='s1',
                         disabled_class=None, link_selected=False):
    from django.utils.safestring import mark_safe
    from django.utils.html import escape
    label = mark_safe(escape(option.label))
    if option.disabled:
        if disabled_class == 'span':
            label = '<span>%s</span>' % label
        return u'<li class="s5">%s</li>' % (label)
    if option.selected():
        if link_selected:
            label = u'%s' % label
        return u'<li class="%s"><a href="%s">%s</a></li>' % (
            selected_class, option.href(), label)
    else:
        return u'<li><a href="%s">%s</a></li>' % (option.href(), label)


def get_page_link(filter, index, label, disabled_if_selected=False):
    from django.utils.safestring import mark_safe
    from django.utils.html import escape
    label = mark_safe(escape(label))
    if filter.options[index].disabled:
        return '<li class="s5">%s</li>' % (label)
    if index == filter.get_page_index():
        if disabled_if_selected:
            return '<li class="s5">%s</li>' % (label)
        else:
            return '<li class="s1">%s</li>' % (label)
    else:
        return '<li><a href="%s">%s</a></li>' % (
            filter.options[index].href(), label)
