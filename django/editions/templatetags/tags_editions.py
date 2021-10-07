# -*- coding: utf-8 -*-
from django import template
import re
from django.utils.http import urlquote
from django.utils.html import escape

register = template.Library()


@register.filter
def link_to_standard_editions(xml, version):
    ''' Convert <li>Liebermann [...]</li>
        to a <li><a href="[link to this version in Liebermann /laws/manuscript/liebermann/?tp=ob&nb=[cn-1018]]">Liebermann [...]</a></li>
        --
        Basically we detect the items in the list which contains the slug of a standard edition.
    '''
    from editions.models import Witness, Manuscript

    standard_editions = Manuscript.objects.filter(standard_edition=True)
    for standard_edition in standard_editions:
        if Witness.objects.filter(manuscript=standard_edition, version=version).count():
            link = '/laws/manuscripts/%s?tp=ob&nb=%s' % (
                standard_edition.slug.lower(), version.slug)
            xml = re.sub(ur'(?musi)<li>([^<]*%s.*?)</li>' % standard_edition.slug.lower(), ur'<li><a href="%s">\1</a></li>' % link, xml)
    return xml


@register.filter
def dblinks(text):
    # <span class="cch-rresource tei-ref teia_type__resource teia_rid__1">Vitrail</span>
    # =>
    # <img src="MEDIA_PATH/MEDIA_FILE"/>
    links = re.findall(
        '(<span class="cch-rresource\s[^"]*\steia_rid__(\d+)">(.*?)</span>)', text)
    # [(u'<span class="cch-rresource tei-ref teia_type__resource teia_rid__1">Vitrail</span>', u'1', u'Vitrail')]
    from editions.models import Resource
    for link in links:
        img_html = ''
        # get the resource record
        resource = Resource.objects.filter(id=link[1])
        if resource.count() == 1:
            resource = resource[0]
            if re.match('.*\.(jpg|gif|tif|bmp|png)$', resource.file.url):
                img_html = '''<div class="eel-image">
                    <img title="%s" src="%s"/>
                    <p>%s</p>
                </div>''' % (escape(resource.title), urlquote(resource.file.url), escape(resource.caption))
            if re.match('.*\.(pdf|doc)$', resource.file.url):
                img_html = '''<a class="pdf-link" title="%s" href="%s" target="_blank">
                    %s
                </a>''' % (escape(resource.title), urlquote(resource.file.url), escape(link[2]))
            text = text.replace(link[0], img_html)
    return text


@register.simple_tag
def bib_entry(bibliographic_entry):
    '''<p><div class="tei-bibl"><span class="tei-author">Alexander, L. M.</span>,
        <span class="tei-title teia-level__a">The legal status of the native Britons in late seventh-century
        Wessex as reflected by the Law Code of Ine</span>,
        <span class="tei-title teia-level__m"><em>Haskins Society Journal</em></span>, 7
        (<span class="tei-date">1995</span>), 31-8.</div></p>'''
    '''<li class="r02 c01 z02"><span class="s01">Amt, E.</span>
        'Richard de Lucy, Henry II's justiciar', <span class="s02">Medieval Prosopography</span>, 9 (1988), 61-87</li>
    '''
    ret = ''
    ret = bibliographic_entry.styled_reference
    ret = re.sub('(?sui)</?p[^>]*>', '', ret)
    ret = re.sub('(?sui)</?div[^>]*>', '', ret)

    # [nospace],[space]
    ret = re.sub('(?sui)\s*,\s*', ', ', ret)
    # [space]([nospace]
    ret = re.sub('(?sui)\s*\(\s*', ' (', ret)

    ret = re.sub('(?sui)tei-editor', 's01', ret)
    ret = re.sub('(?sui)tei-author', 's01', ret)
    ret = re.sub('(?sui)tei-title teia-level__m', 's02', ret)
    ret = re.sub(
        '(?sui)<span class="tei-title teia-level__a">([^<]*)</span>', r'\1', ret)
    ret = re.sub('(?sui)<span class="tei-date">([^<]*)</span>', r'\1', ret)

    new_entry = False
    from gsettings.gvars import get_value
    duration = get_value('bib_novelty_duration')
    if bibliographic_entry.created is not None and duration is not None:
        from datetime import date
        new_entry = (
            (date.today() - bibliographic_entry.created).days < duration)

        if new_entry:
            ret = ret + '<span class="new-bib-entry">New entry</span>'

    return ret


@register.filter
def djatoka_encode(value):
    from django.utils.http import urlquote
    # fix the urlencoding so Djatoka is happy.
    #
    # I still don't really understand what the problem is.
    # What I've noticed is that if we get a space in the url, we need to encode it as %2520 not just %20
    # %20 is the url encoding for space. And %3520 is the url encoding for '%20'
    #
    # This works:
    #     http://localhost:8080/adore-djatoka/resolver?url_ver=Z39.88-2004&rft_id=http%3A%2F%2Fimages.cch.kcl.ac.uk%2Feel%2Fincoming%2F%2Fbatch1-jpg%2FDurham%20AIV19%2Fff.48r.jpg&svc_id=info:lanl-repo/svc/getRegion&svc_val_fmt=info:ofi/fmt:kev:mtx:jpeg2000&svc.format=image/jpeg&svc.scale=0,300
    # This doesn't:
    #     http://localhost:8080/adore-djatoka/resolver?url_ver=Z39.88-2004&rft_id=http%3A%2F%2Fimages.cch.kcl.ac.uk%2Feel%2Fincoming%2F%2Fbatch1-jpg%2FDurham%2520AIV19%2Fff.48r.jpg&svc_id=info:lanl-repo/svc/getRegion&svc_val_fmt=info:ofi/fmt:kev:mtx:jpeg2000&svc.format=image/jpeg&svc.scale=0,300
    #

    # no longer needed for loris?
    # return urlquote(value).replace('%20', '%2520')
    return value


@register.simple_tag
def folio_pair_location(pair, single_sheet=False):
    ret = 'N/A'
    if pair is not None:
        ret = ''
        no_prefix = False
        for i in ['0', '1']:
            if pair[i] is None:
                if not single_sheet:
                    ret = ret + 'n/a'
            else:
                no_prefix = True
                ret = ret + pair[i].get_display_location(no_prefix)
            if i == '1':
                break
            # don't show range end if same as range start
            if pair['0'] == pair['1']:
                break
            # avoid duplicating the label A - A. Unfortunately I cannot
            # remember under which conditions this might happen.
            if pair['0'] is not None and pair['1'] is not None and (not pair['0'].page) and pair['0'].folio_number == pair['1'].folio_number and pair['0'].folio_side == pair['1'].folio_side:
                break
            if not single_sheet:
                ret = ret + ' - '

    return ret
