# -*- coding: utf-8 -*-
from models import *
import re
from django import http, template
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy, ugettext as _
from django.utils.safestring import mark_safe
from cch.views import utils as view_utils
from xml.dom import minidom
#log.log(text, 2)
from cch.logger.log_file import log
from django.contrib.admin.views.decorators import staff_member_required
from cch.views.utils import get_template, get_json_response
import simplejson as json

from django.http import HttpResponse, Http404
from editions.models import get_source_abbreviations
from editions.models_generic import Witness
from os import removedirs

# --------------------------------------------------------------------------


def edition_text_test_view(request, editionid):
    context = {}
    context['edition'] = Edition.objects.get(id=editionid)
    # get the xml of the text
    # text = context['edition'].rendered_text
    import time
    context['unique_number'] = time.time()
    panel_index = '0'
    context['text'] = re.sub(
        ur'#p#',
        '%s' %
        panel_index,
        context['edition'].rendered_edition)
    return get_template('admin/editions/edition_test', context, request)


###################################################
#                     PREVIEWS
###################################################

def edition_witness_translation_preview_view(request, witnessid):
    return edition_witness_transcription_preview_view(request, witnessid, True)


def edition_witness_transcription_preview_view(
        request, witnessid, request_translation=False):
    # *WTC, *WTL, *CA
    witness = Witness.objects.get(id=witnessid)
    witness_transcription = get_witness_transcription(witnessid)
    witness_translation = get_witness_translation(witnessid)
    editions = Edition.objects.filter(
        version=witness.version.all()[0])
    edition = editions[0]

    if request_translation:
        requested_record = witness_translation
    else:
        requested_record = witness_transcription

    columns = get_preview_default_columns()

    # columnm 3 is the text of the translation
    columns[3] = columns[2]
    columns[1] = {
        'label': 'Transcription',
        'key': 'text',
        'rec': witness_transcription
    }
    columns[2] = {
        'label': 'Translation',
        'key': 'text',
        'rec': witness_translation
    }

    return record_preview_view(request, edition, requested_record, columns)


def edition_translation_preview_view(request, editionid):
    edition = Edition.objects.get(id=editionid)
    requested_record = edition.edition_translation

    columns = get_preview_default_columns()

    # columnm 3 is the text of the translation
    columns[2] = {
        'label': 'Translation of edition',
        'key': 'text',
        'rec': requested_record
    }

    return record_preview_view(request, edition, requested_record, columns)


def edition_text_preview_view(request, editionid):
    edition = Edition.objects.get(id=editionid)
    requested_record = edition

    columns = get_preview_default_columns()

    return record_preview_view(request, edition, requested_record, columns)


def get_preview_default_columns():
    return [
        {'label': 'Unit', 'key': 'lvl'},
        {'label': 'Edition', 'key': 'text'},
        {'label': 'Apparatus', 'key': 'cas'},
        {'label': 'Commentary', 'key': 'commentary'},
    ]


def record_preview_view(request, edition, requested_record, columns):
    '''
    Preview a text in a table format.

    The text structure is 'flatten' in to a sequence of text units.
    Each unit i a seaprate row.
    The first column is always the unit ID (e.g. prol).

    The content of the following columns depend on the requested document:

    1. Edition:
        ETC, CA, COM
    2. Translation of Edition:
        ETC, *ETL, *COM
    3. Witness Transcription (or Translation):
        *WTC, *WTL, *CA

    (ETC: edition, ETL: transl of edition, CA: crit app, COM: commentaries,
    WTC: witness transc., WTL: witness transl)
    '''

    # doc_type = text|translation

    context = {}

    # key: see dict returned by get_flat_parts_from_xml()
    # rec: which record the value is taken from (default = edition)
    context['cols'] = columns

    # read all commentaries for this edition
    commentaries = {}
    for c in Commentary.objects.filter(edition=edition):
        commentaries[c.elementid] = c

    # get all abbreviated sources (used to expand crit. apparatus)
    source_abbreviations = get_source_abbreviations()

    # gather all the data needed to populate the table
    rows = {}
    records = {}
    for col in context['cols']:
        record = col.get('rec', edition)

        if id(record) not in records:
            # gather data from a record
            records[id(record)] = record
            text_dom = get_dom_from_text(record.text)

            units = []
            get_units_from_xml(
                text_dom.documentElement,
                units,
                source_abbreviations,
                commentaries
            )

            # populate the rows with data from this record
            for unit in units:
                sortableid = unit['sortableid']
                if sortableid not in rows:
                    # create the row
                    rows[sortableid] = ['?'] * len(context['cols'])

                # fill in the relevant columns
                row = rows[sortableid]
                for i, col in enumerate(context['cols']):
                    if col.get('rec', edition) == record:
                        row[i] = unit.get(col['key'])

    # convert rows to a sorted
    context['rows'] = []
    for sortableid in sorted(rows.keys()):
        context['rows'].append(rows[sortableid])

    context.update(get_context_labels_from_record(requested_record))

    return get_template('admin/editions/edition_preview', context, request)


def get_units_from_xml(
        node, units, source_abbreviations, commentaries, parent_part=None):
    '''
    node: a minidom xml node
    part: a (flat) list of parts
    parent_part: the part for the parent of <node> (for internal use only)

    The function recursively drills into node and its children.
    It adds a metadata dictionary to parts each time a new text unit is found.
    '''

    part = parent_part

    if node.nodeType != minidom.Node.ELEMENT_NODE:
        return part

    tag = node.tagName.lower()
    nodeid = node.getAttribute('id')
    aclass = node.getAttribute('class')

    if not nodeid and tag in ['doc']:
        nodeid = 'doc'
        aclass = 'tei-div'

    new_part = tag in ['p', 'div', 'doc'] and nodeid
    if new_part:
        # new part (or unit of text)
        part = {
            'text': '',
            'id': nodeid,
            'commentary': '',
            'cas': '',
            'parent': part,
        }

        part.update(get_info_from_xml_element(node))

        # lvl_abs is an global/absolute position in the hierarchy
        # it is (string-)sortable and used to match units from different
        # documents (e.g. transl & transc).
        # e.g. 'c1p1' for code 1, prol 1
        if part['parent']:
            part['sortableid'] = part['parent']['sortableid'] + part['sortableid']

        part['text'] = node.toxml()
        units.append(part)

    # add commentary
    if nodeid in commentaries:
        part['commentary'] += commentaries[nodeid].text

    # add critical apparatus
    ca = re.findall(ur'teia-readings__([^ "]*)', aclass or '')
    if ca:
        part['cas'] += get_string_from_html_encoded_critical_apparatus(
            ca, source_abbreviations)

    # process all children
    to_remove = []
    to_clone = []
    for child in node.childNodes:
        child_part = get_units_from_xml(
            child, units, source_abbreviations, commentaries, part)
        if child_part != part:
            to_remove.append(child)
        elif to_remove:
            hole = True

    # That's the clever part. Without this all parent would contain the
    # xml of all descendants even those which are turned into parts.
    for child in to_remove:
        node.removeChild(child)

    part['text'] = node.toxml()

    return part


def get_info_from_xml_element(node):
    '''
    node: a minidom element that correspond to a unit of text (e.g. chapter)

    e.g. <div class="teia-type__chapter teia-n__2">

    returns
    {
        'type': 'chapter'
        'n': '2'
        # a short relative label
        'lvl': 'chap 2'
        # a relative & sortable code
        'sortableid': 'c2'
    }
    '''

    ret = {
        'n': '0',
        'type': '?',
        'lvl': '',
        'sortableid': '',
    }

    if node.tagName.lower() == 'doc':
        ret['type'] = 'document'
    else:
        aclass = node.getAttribute('class')
        if aclass:
            atype = re.findall(ur'.*teia-type__(\w+).*', aclass)
            if atype:
                ret['type'] = atype[0]
            anum = re.findall(ur'.*teia-n__(\w+).*', aclass)
            if anum:
                ret['n'] = anum[0]

    ret['lvl'] = (ret['type'][:4] + ' ' + ret['n']).strip()

    # Capitalise 'P'ROLOGUE so it comes before 'c'hapter in the code
    ret['sortableid'] = ret['type'][0] + ret['n']
    if ret['type'].startswith('prol'):
        ret['sortableid'] = ret['sortableid'].upper()

    return ret

##################################################
#        TEXT EDITORS
##################################################


def witness_transc_text_view(request, witnessid):
    record = get_witness_transcription(witnessid)
    return record_text_view(request, record)


def witness_transl_text_view(request, witnessid):
    record = get_witness_translation(witnessid)
    return record_text_view(request, record)


def get_witness_transcription(witnessid):
    witness = Witness.objects.get(id=witnessid)
    if witness.witness_transcription is not None:
        record = witness.witness_transcription
    else:
        # create record and attach it to the edition
        record = Witness_Transcription()
        record.save()
        witness.witness_transcription = record
        witness.save()
    return record


def get_witness_translation(witnessid):
    transcription = get_witness_transcription(witnessid)
    if transcription.witness_translation is not None:
        record = transcription.witness_translation
    else:
        # create record and attach it to the edition
        record = Witness_Translation()
        record.save()
        transcription.witness_translation = record
        transcription.save()
    return record


def edition_download_view(request, editionid):
    from datetime import date
    from cch.views import utils
    import os

    edition = Edition.objects.get(id=editionid)

    # generate file prefix
    prefix = 'eel-%s-%s-%s' % (
        editionid,
        edition.version.slug,
        date.today().isoformat()
    )

    # re-create dir
    dir_name = prefix
    dir_path = os.path.join(settings.WEBSITE_ROOT, dir_name)

    utils.removetree(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    def save_xml(record, dir_path, prefix, suffix, field_name='text'):
        if not record:
            return
        xml_string = getattr(record, field_name, ur'').strip()
        if not xml_string:
            return
        filepath = os.path.join(dir_path, prefix + ur'-' + suffix) + '.xml'
        content = xml_string
        content = ur'<doc>%s</doc>' % content
        utils.write_file(filepath, content)

    # Save xmls in directory
    save_xml(edition, dir_path, prefix, 'introduction', 'introduction')
    save_xml(edition, dir_path, prefix, 'edition')
    save_xml(edition.edition_translation, dir_path, prefix, 'translation')
    for witness in edition.version.get_witnesses():
        prefix_witness = ur'-'.join([
            prefix,
            slugify(unicode(witness.manuscript.sigla)),
            slugify(unicode(witness.manuscript.shelf_mark)),
        ])
        trans = witness.witness_transcription
        save_xml(
            trans,
            dir_path,
            prefix_witness,
            'transcription')
        if trans:
            save_xml(
                trans.witness_translation,
                dir_path,
                prefix_witness,
                'translation')

    #save_xml(edition.edition_translation, dir_path, prefix, 'edition')

    # zip the directory
    zip_file = '%s.zip' % prefix
    zip_path = '%s.zip' % dir_path
    if os.path.exists(zip_path):
        os.unlink(zip_path)
    command = '''zip -j -rm %s %s''' % (zip_path, dir_path)
    os.system(command)

    utils.removetree(dir_path)

    return utils.get_file_response(zip_file, zip_path)


def edition_text_view(request, editionid):
    record = Edition.objects.get(id=editionid)
    return record_text_view(request, record)


def edition_trans_text_view(request, editionid):
    edition = Edition.objects.get(id=editionid)
    if edition.edition_translation is not None:
        record = edition.edition_translation
    else:
        # create record and attach it to the edition
        record = Edition_Translation()
        record.save()
        edition.edition_translation = record
        edition.save()
    return record_text_view(request, record)


@staff_member_required
def record_text_view(request, record):
    if len(request.REQUEST.get('action', '')) > 0:
        return record_text_ajax(request, record)

    from django.template.context import Context
    context = {'wysiwyg_fields': 'text_boxid',
               'wysiwyg_fields_custom': 'text_boxid'}
    context['wysiwyg_fields_custom_buttons1'] = 'undo,redo,separator,CCHclear,separator,code,separator,save'
    context['wysiwyg_fields_custom_buttons2'] = 'TEIcode,TEIbook,TEIprologue,TEIchapter,TEIdivision,separator,TEItitle,TEIrubric,separator,TEIforeign,TEIadded,TEIdeleted,TEIgap,TEIsupplied,TEIPb,TEIapparatus,separator,TEIpagebreak,separator'
    context['edition'] = record
    context['selected_divid'] = request.REQUEST.get('div', 'doc')
    context['selected_div'] = get_xml_fragment(
        context['edition'], context['selected_divid'], True)
    context['commentary'] = get_commentary(
        context['edition'], context['selected_divid']).text
    # data structure used by tinymce popup windows (CA and page break)
    context['ca_table_html'] = get_critical_aparatus_table(record)
    context['page_break_info'] = get_page_break_info(record)
    context.update(get_context_labels_from_record(record))
    context['witnesses_list'] = get_witnesses_list()
    context['versions_list'] = get_versions_list()

    return render_to_response('admin/editions/edition_text.html', Context(
        context), context_instance=template.RequestContext(request))


def get_context_labels_from_record(record):
    cls_name = record.__class__.__name__

    ret = {
        'text_label': 'TEXT LABEL',
        'doc_type': cls_name.split('_')[-1],
        # i.e. only edition text itself (not its translation)
        'is_edition': 0,
    }

    if cls_name == 'Edition':
        ret['is_edition'] = 1
        ret['text_label'] = '%s (%s)' % (
            record.version.version_name(),
            record.abbreviation
        )
    if cls_name == 'Edition_Translation':
        ret['text_label'] = '%s (%s)' % (
            record.get_edition().version.version_name(),
            record.get_edition().abbreviation
        )
    if cls_name in ('Witness_Transcription', 'Witness_Translation'):
        ret['text_label'] = unicode(record.getWitness().manuscript)

    ret['text_title'] = '%s of %s' % (ret['doc_type'], ret['text_label'])

    return ret


def get_page_break_info(record):
    # get all the witnesses for this edition
    ret = []
    witnesses = []

    if record.__class__.__name__ == 'Edition':
        witnesses = Witness.objects.filter(
            version=record.version).order_by('manuscript__sigla')
    if record.__class__.__name__ == 'Edition_Translation':
        witnesses = Witness.objects.filter(
            version__edition__edition_translation=record).order_by('manuscript__sigla')
    if record.__class__.__name__ == 'Witness_Transcription':
        witnesses = Witness.objects.filter(
            witness_transcription=record).order_by('manuscript__sigla')
    if record.__class__.__name__ == 'Witness_Translation':
        witnesses = Witness.objects.filter(
            witness_transcription__witness_translation=record).order_by('manuscript__sigla')

    for witness in witnesses:
        pages = witness.get_expanded_range()
        # MS with undefined folio range are filtered out
        if len(pages):
            ret.append({'name': witness.manuscript.sigla,
                        'id': witness.id, 'pages': pages})

    import simplejson as json
    return json.dumps(ret)


def truncate_text(text, l=40):
    ret = text
    if len(ret) > l:
        ret = ret[0:l] + '...'
    return ret


def get_witnesses_list():
    ret = [(w.id, '%s - %s' % (truncate_text(w.work.name), w.manuscript.sigla))
           for w in Witness.objects.all().order_by('work__name')]
    return json.dumps(ret)


def get_versions_list():
    ret = [(w.id, '%s - %s' % (w.standard_abbreviation, truncate_text(w.version_name())))
           for w in Version.objects.all().order_by('standard_abbreviation')]
    return json.dumps(ret)


def get_critical_aparatus_table(record):
    # create the html table for the edition of the critical apparatus
    #
    # ca-r-R ca-d-R-A/W-ID
    #
    # [['fsjka {fskfal}', 'W1', 'W2', 'A1'], ['txt1 {txt2}', 'W3', 'W2', 'A4']]
    #
    ret = ''
    if record.__class__.__name__ == 'Edition':
        texts = [
            {'label': 'MS1', 'id': '1', 'type': 'W'},
            {'label': 'MS2', 'id': '2', 'type': 'W'},
            {'label': 'A1', 'id': '10', 'type': 'A'},
            {'label': 'A2', 'id': '20', 'type': 'A'},
        ]

        texts = []
        for witness in Witness.objects.filter(
                version=record.version).order_by('manuscript__sigla'):
            texts.append({'label': witness.manuscript.sigla,
                          'id': witness.id, 'type': 'W'})
        for archetype in Hyparchetype.objects.filter(
                edition=record).order_by('sigla'):
            texts.append({'label': archetype.sigla,
                          'id': archetype.id, 'type': 'A'})

        rows = ''
        for i in range(0, 7):
            row = ''
            if i == 0:
                for text in texts:
                    row = row + '<td>%s</td>' % text['label']
                rows = rows + '<tr><td>Reading</td>%s</tr>' % (row,)
            else:
                for text in texts:
                    row = row + \
                        '<td><input name="ca-d-%s-%s-%s" type="checkbox"></td>' % (
                            i, text['type'], text['id'])
                rows = rows + \
                    '<tr><td><input name="ca-r-%s" type="text"/></td>%s</tr>' % (
                        i, row)

        # get all the witnesses and archetypes
        ret = '''<table>
                %s
                </table>''' % rows

    return ret


def record_text_ajax(request, record):
    action = request.REQUEST.get('action', '')
    divid = request.REQUEST.get('divid', None)
    json_list = {'error': 'unknown action (%s)' % action}

    if record:
        if action == 'load_text':
            com_record = get_commentary(record, divid)
            json_list = {
                'selected_div': get_xml_fragment(
                    record,
                    divid,
                    True),
                'commentary': com_record.text}

        if action == 'save_text':
            text = request.REQUEST.get('text', None)
            #edition_id = request.REQUEST.get('editionid', None)
            # save the commentary
            commentary = request.REQUEST.get('commentary', None).strip()
            if commentary is not None and divid:
                com_record = get_commentary(record, divid)
                if com_record.id and not commentary:
                    com_record.delete()
                if commentary:
                    from datetime import datetime
                    com_record.updated = datetime.now()
                    com_record.user = get_current_user(request)
                    com_record.text = commentary
                    com_record.save()

            # save the text
            if text is not None:
                if not divid:
                    text = None
                    json_list = {
                        'error': 'save failed (divid not specified %s)' % repr(divid)
                    }
                elif divid != 'doc':
                    # 'doc' is a special id which refers to the whole xml document
                    # Only one div has changed
                    # Let's replace it within the whole xml document
                    text_dom = get_dom_from_text(record.text)
                    div_node = text_dom.getElementById(divid)
                    if div_node:
                        # remove children
                        while div_node.hasChildNodes():
                            div_node.removeChild(div_node.firstChild)

                        '''
                        insert submitted sub-tree
                        first we remove any block elements if we are about to
                        insert into a span. Otherwise ff or other browser will
                        move thing round with unpleasant results.
                        typical case: if we insert a <p> into a parent <span>
                        then we load the whole document => firefox will move
                        the p out of the span
                        '''
                        if div_node.tagName.lower() == 'span':
                            text = re.sub(ur'(?us)</?p>', ur'', text)
                            text = re.sub(ur'(?us)</?div>', ur'', text)

                        new_div_dom = get_dom_from_text(text, True)
                        for node in new_div_dom.documentElement.childNodes:
                            div_node.appendChild(node)
                        text = text_dom.documentElement.toxml()
                    else:
                        text = None
                        json_list = {
                            'error': 'save failed (%s not found)' % divid}
                if text:
                    record.text = get_clean_html(text)
                    div_tree = add_div_numbers(record)
                    record.save()
                    json_list = {'tree': div_tree}

        if action == 'update_div_number':
            number = request.REQUEST.get('number', 0)
            div_tree = add_div_numbers(record, divid, number)
            record.save()
            json_list = {'tree': div_tree}

        if action == 'get_structure':
            text = record.text
            dom = get_dom_from_text(text)
            json_list = {
                'tree': get_divs_tree(
                    dom.documentElement,
                    False,
                    record
                )
            }

    return get_json_response(json_list)


def get_current_user(request):
    ''' return admin user instead of anonymous user
        because anonymous user cannot be assigned to the foreign key (django error)
    '''
    ret = request.user
    from django.contrib.auth.models import User
    if ret and ret.is_anonymous():
        ret = User.objects.get(id=1)
    return ret


def get_commentary(record, elementid):
    ''' returns a commentary object attached to an element in an edition.
        return a default commentary object if not found in the database (.id is None).
    '''
    # get the commentary record
    if record.__class__ == Edition:
        edition = record
    else:
        # !!! More than one edition can be linked to a Witness !!!
        if record.__class__ == Witness_Translation:
            w = Witness.objects.filter(
                witness_transcription__in=[
                    wtc for wtc in Witness_Transcription.objects.filter(
                        witness_translation=record)])
            wv = Version_Witness.objects.filter(witness=w[0])
            edition = Edition.objects.filter(
                version__in=[
                    wv.version for wv in Version_Witness.objects.filter(
                        witness=w[0])])
        if record.__class__ == Witness_Transcription:
            w = Witness.objects.filter(witness_transcription=record)
            wv = Version_Witness.objects.filter(witness=w[0])
            edition = Edition.objects.filter(
                version__in=[
                    wv.version for wv in Version_Witness.objects.filter(
                        witness=w[0])])
        if record.__class__ == Edition_Translation:
            edition = Edition.objects.filter(edition_translation=record)
        edition = edition[0]
    ret = Commentary.objects.filter(edition=edition, elementid=elementid)
    # create it if it does not already exists
    if ret.count() == 0:
        ret = Commentary()
        ret.edition = edition
        ret.elementid = elementid
        ret.text = ''
    else:
        ret = ret[0]
    return ret


def add_div_numbers(record, updated_divid=0, updated_number=0):
    '''
    reassign all div numbers in sequence
    # returns a tree with the hierarchy of divs and their numbers

    # Automatically populate the n attribute of the tei div elements.
    # Don't override existing values.
    # Take the type of div into account prol., prl., chp., chp. => 1,2,1,2
    # Return the updated div tree
    '''

    text_dom = get_dom_from_text(record.text)
    ret = None

    if text_dom is not None:

        def assign_div_numbers(div_tree, dom):
            type_previous = '123'
            number = 0
            renumber_divs_following_updated_div = False
            if 'children' in div_tree:
                for div in div_tree['children']:
                    # number is the new number
                    # reset the counter if the type of the div changes
                    # e.g. prol, prol, chap, chap => 1,2,1,2
                    if div['type'] != type_previous:
                        number = 0
                        if div['type'] == 'division':
                            number = -1
                    number += 1

                    # get the current number
                    current_number = 0
                    if 'n' in div:
                        try:
                            current_number = int(div['n'])
                        except Exception:  # current_number = None
                            pass

                    # Case where the user inserts a new div in an already numbered block
                    # Original seq. of divs: 1,2,3;
                    # User inserts new div => 1,None,2,3;
                    # Auto Numbering: 1,2,2,3 - we detects 2,2 and increment it
                    # => 1,2,3,3; and so on => 1,2,3,4
                    if (not renumber_divs_following_updated_div) and (
                            current_number > number):
                        # don't change existing numbers
                        number = current_number

                    # update the number in the xml document
                    if 'id' in div and div['id']:
                        if div['id'] == updated_divid:
                            # update the number of a specific div
                            number = int(updated_number)
                            renumber_divs_following_updated_div = True
                        if (current_number != number):
                            div_node = dom.getElementById(div['id'])
                            set_TEI_attribute(div_node, 'n', number)
                            div['n'] = number

                    # recursion for the kids
                    assign_div_numbers(div, dom)

                    type_previous = div['type']

        # go through all the divs in the tree and update their number
        ret = get_divs_tree(text_dom, False, record)
        assign_div_numbers(ret, text_dom)

        record.text = text_dom.documentElement.toxml()

    return ret


def get_TEI_attribute(element, name, default=''):
    v = element.getAttribute('class')
    if v is None:
        v = ''
    ret = re.sub(ur'^.*teia-%s__(\S*).*$' % name, ur'\1', v)
    if len(ret) == len(v):
        ret = default
    return ret


def set_TEI_attribute(element, name, value):
    pattern = 'teia-%s__' % name
    new_value = '%s%s' % (pattern, value)

    # remove old attribute
    v = element.getAttribute('class')
    if v is None or v == '':
        v = ''
    else:
        v = re.sub(ur'(?us)' + pattern + '\S*', '', v)

    # add the new one
    element.setAttribute('class', v.strip() + ' ' + new_value)


def get_divs_tree(anode, internal_call=False,
                  edition=None, commentaryids=None):
    '''
    Returns the tree of tei divs from an xml node. This is recursive dictionary.

    - updated_divid=0, updated_number=0 are only used by some functions which need to update
    the number of particular tei div.
    '''
    tree = []

    if commentaryids is None:
        commentaryids = [
            c.elementid for c in Commentary.objects.filter(
                edition=edition)]

    for node in anode.childNodes:
        if node.nodeType == 1:
            # node.tagName
            item = {
                'tag': '',
                'n': 0,
                'id': '',
                'type': 'division',
                'children': get_divs_tree(
                    node,
                    True,
                    edition,
                    commentaryids)}
            class_attr = node.getAttribute('class')
            if class_attr:
                item['id'] = node.getAttribute('id')
                if item['id'] in commentaryids:
                    item['co'] = 1
                # decode the attributes - 'tei-div teia-type__chapter'
                s = re.search(ur'(?iu)tei-([^\s]*)', class_attr)
                if s is not None:
                    item['tag'] = s.group(1)
                s = re.findall(ur'(?iu)teia-([^\s_]*)__([^\s_]*)', class_attr)
                if s is not None:
                    for pair in s:
                        item[pair[0]] = pair[1]
            if item['tag'] not in ['div']:
                # not a tei 'div' => its children are promoted to this level
                for sub_item in item['children']:
                    tree.append(sub_item)
            else:
                # the current node is a tei div
                if len(item['children']) == 0:
                    # slight compression of the leaves
                    del item['children']
                tree.append(item)
    if not internal_call:
        # returns the root of the tree
        tree = {
            'tag': 'div',
            'type': 'Complete document',
            'n': '',
            'id': 'doc',
            'children': tree}
        if 'doc' in commentaryids:
            tree['co'] = 1

    return tree


''' Returns a DOM from a given xml string. The dom will have a root element called 'doc' '''


def get_dom_from_text(text, adecode_entities=False, is_clean=False):
    # second line is needed to make minidom understand that 'id' is the ID
    # attribute. (getElementById wouldn't work otherwise)
    text = u'''<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE div [<!ATTLIST div id ID #IMPLIED> <!ATTLIST span id ID #IMPLIED>]>
    <doc>%s</doc>''' % text

    if not is_clean:
        text = get_clean_html(text)

    dom = minidom.parseString(text.encode('utf-8'))

    return dom

##
# From: http://effbot.org/zone/re-sub.htm#unescape-html
# October 28, 2006 | Fredrik Lundh
# Removes HTML or XML character references and entities from a text string.
# Leave the 5 predefined XML entities as they are (',",&,<,>).
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.


def get_xml_fragment(record, divid, inside=False):
    ret = get_clean_html(record.text)
    if divid:
        dom = get_dom_from_text(ret)
        node = dom.getElementById(divid)
        if node is not None:
            ret = node.toxml()

    if inside and ret:
        # remove the first opening tag and the last closing tag
        ret = re.sub(r'(?us)^[^>]*>(.*)<[^<]*$', r'\1', ret)

    return ret
