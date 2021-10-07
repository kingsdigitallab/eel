import re
from django import http, template
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.contrib import admin
import db_ids
from django.conf import settings
from cch.views.utils import get_template, get_json_response, get_concat_from_field_names
from views_utils import get_page_not_found

from django.http import HttpResponse, Http404
from django.template.defaultfilters import slugify


def introduction_view(request, slug=None):
    from models import Version, Edition, Witness
    context = {}
    versions = Version.objects.filter(slug=slugify(slug))
    if versions.count() > 0:
        version = versions[0]
        context = {'version': version}
        context['edition'] = version.get_an_edition()
        context['witnesses'] = Witness.objects.filter(
            version=version,
            manuscript__standard_edition=False).order_by('manuscript__sigla')
        context['other_versions'] = Version.objects.filter(
            work=version.work).exclude(
            id=version.id).order_by('standard_abbreviation')
        return get_template('website/introduction', context, request)
    else:
        return get_page_not_found(request)

#@staff_member_required


def bibliography_view(request, url=None):
    '''record_type = {author, play, translator} '''
    from editions.models import Bibliographic_Entry, Bib_Category

    context = {'page_title': 'Bibliography'}

    from cch.page_filters.page_filters import Filter, get_az_filter
    context['biblio_types'] = Filter('Bilio type', 'tp', request, 'tab', ((
        'By Category', 'c'), ('By Author', 'a'), ('By Year', 'y')))

    if context['biblio_types'].get_value() == 'c':
        context['categories'] = Filter(
            'Categories', 'ct', request, 'box1core', [
                (cat.name, cat.id) for cat in Bib_Category.objects.all().order_by('name')])
        context['categories'].set_default_option(db_ids.BIB_CATEGORY_GENERAL)
        catid = int(context['categories'].get_value())
        context['records'] = Bibliographic_Entry.objects.filter(
            bib_category__id=catid).order_by(
            'authors', 'title_article', 'title_monograph')

    if context['biblio_types'].get_value() == 'a':
        context['authors'] = get_az_filter(
            request, 'editions_bibliographic_entry', ['authors'])
        context['records'] = Bibliographic_Entry.objects.filter(
            authors__istartswith=context['authors'].get_value()).order_by(
            'authors', 'title_article', 'title_monograph')

    if context['biblio_types'].get_value() == 'y':
        context['date_ranges'] = Filter(
            'Date range', 'dr', request, 'tab', [
                (year, year) for year in range(
                    2010, 1870, -10)])
        decade = int(context['date_ranges'].get_value())
        context['years'] = []
        for year in range(decade + 9, decade - 1, -1):
            records = Bibliographic_Entry.objects.filter(
                publication_date=year).order_by(
                'authors', 'title_article', 'title_monograph')
            if records.count():
                context['years'].append({'year': year, 'records': records})

    return get_template('website/bibliography', context, request)


def glossary_view(request, url=None):
    '''record_type = {author, play, translator} '''
    from editions.models import Glossary_Term

    context = {'page_title': 'Glossary'}

    from cch.page_filters.page_filters import Filter, get_az_filter

    context['letters'] = get_az_filter(
        request, 'editions_glossary_term', ['term'])
    context['records'] = Glossary_Term.objects.filter(
        term__istartswith=context['letters'].get_value()).order_by('term')

    return get_template('website/glossary', context, request)


def blog_view(request, url=None):
    return redirect('http://blog.earlyenglishlaws.ac.uk/')


def relationships_view(request, slug=None):
    from editions.models import Version, Version_Relationship, Version_Relationship_Type, Work, Language
    from django.db.models import Q
    context = {}

    rel_data = {
        'texts': {},
        'links': {},
        'languages': {},
        'rel_types': {},
    }

    def get_graph_from_version(version0):
        ret = version0.get_graph()
        if ret is None:
            ret = {
                'texts': {},
                'links': {},
                'languages': {},
                'rel_types': {},
            }
            return ret

        # 1. texts
        versions = Version.objects.filter(id__in=ret['texts'].keys())
        for version in versions:
            v = ret['texts']['%s' % version.id]
            king_name = ''
            king = version.get_a_king()
            if king is not None:
                king_name = king.name
            v['short_title'] = version.standard_abbreviation
            v['title'] = version.version_name()
            v['slug'] = version.slug
            v['id'] = version.id
            v['languageid'] = version.get_a_language().id
            v['king'] = king_name
            v['date'] = '%s' % version.date

        # 1. links
        links = Version_Relationship.objects.filter(id__in=ret['links'].keys())
        for link in links:
            l = ret['links']['%s' % link.id]
            l['description'] = link.description
            l['typeid'] = link.version_relationship_type.id

        # 3. language list
        for language in Language.objects.all().order_by('id'):
            ret['languages'][language.id] = {
                'name': language.name, 'color': language.color}

        # 4. rel type list
        for rel_type in Version_Relationship_Type.objects.all().order_by('id'):
            ret['rel_types'][rel_type.id] = {'name': rel_type.name}

        return ret

    versions = Version.objects.filter(slug=slug)
    if versions.count() > 0:
        import simplejson as json
        version = versions[0]
        context['version'] = version
        graph = get_graph_from_version(version)
        context['image_height'] = graph['image']['height']
        context['image_width'] = graph['image']['width']
        context['rel_data'] = json.dumps(graph)
        context['languages'] = graph['languages']

    return get_template('website/relationships', context, request)


def xmod_redirect_view(request, url=None, file=None):
    ''' support for old style urls (.html, etc.) '''
    if (url is None or len(url) == 0 or url == 'index.html'):
        return redirect('/')
    if (file is None or len(file) == 0 or file == 'index'):
        return redirect('/' + url + '/')
    else:
        return redirect('/' + url + '/' + file + '/')


def synopsis_view(request, slug=''):
    return redirect('/laws/texts/%s/' % slug)

    from models import Version, Edition
    versions = Version.objects.filter(slug=slug)
    if versions.count() > 0:
        version = versions[0]
        context = {'version': version}
        editions = Edition.objects.filter(version=version)
        if editions.count() > 0:
            context['edition'] = editions[0]
        return get_template('website/synopsis', context, request)
    else:
        return get_page_not_found(request)


def test_view(request):
    context = {}
    return get_template('website/folio_zoom_test', context, request)
    #return get_template('website/folio_zoom', context, request)


def manuscript_view(request, slug=''):
    from models import Manuscript

    slug = slugify(slug)

    manuscripts = Manuscript.objects.filter(slug=slug)
    if manuscripts.count() > 0:
        manuscript = manuscripts[0]

        # ! these two values must agree with the values set in the javascript file
        default_image_height = 400
        zoom_level_pixel = 50
        if 'zl' in request.COOKIES:
            default_image_height = default_image_height + \
                20 * int(request.COOKIES['zl'])

        context = {}
        ajax = request.REQUEST.get('action', 0)

        from cch.page_filters.page_filters import Filter
        context['manuscript_views'] = Filter(
            'MS views', 'tp', request, 'tab', (('Description', 'd'), ))
        if manuscript.checked_folios and (
                manuscript.standard_edition or not manuscript.hide_from_listings):
            context['manuscript_views'].add_options(
                (('Open book', 'ob'), ('Close up', 's')))

        context['manuscript'] = manuscript
        context['current_pair'] = get_image_pair_from_reference(
            request.REQUEST.get('nb', 0), manuscript)
        context['witnesses'] = get_enriched_witnesses(context)
        context['image_server_url'] = settings.IMAGE_SERVER_URL
        context['folio_size'] = {'height': default_image_height}
        context['folio_size']['width'] = int(
            context['folio_size']['height'] * 220.0 / 300.0)
        context['single_sheet'] = 0
        if manuscript.is_single_sheet():
            context['single_sheet'] = 1

        template_name = 'website/manuscript'
        if request.REQUEST.get('zoom', 0):
            context['image_url'] = context['current_pair']['selected'].get_image_url()
            template_name = 'website/folio_zoom'

        if ajax:
            # if ajax request we return a json response
            pair = context['current_pair']
            ajax_ret = {
                'images':
                [
                    {'url': '', 'id': ''},
                    {'url': '', 'id': ''},
                ],
                # prev and next
                'buttons': [pair['previousid'], pair['nextid']],
                'laws': [],
                'pairid': pair['id'],
            }

            i = 0
            from templatetags.tags_editions import djatoka_encode
            for i in [0, 1]:
                img = pair[str(i)]
                if img is not None:
                    ajax_ret['images'][i] = {
                        'url': djatoka_encode(
                            img.get_image_url()), 'id': img.id}
                i = i + 1
            for witness in context['witnesses']:
                if witness.on_screen:
                    for version in witness.get_versions():
                        ajax_ret['laws'].append(version.standard_abbreviation)

            return get_json_response(ajax_ret)
        else:
            return get_template(template_name, context, request)
    else:
        return get_page_not_found(request)


def get_enriched_witnesses(context):
    ''' Returns a list of Witness object related to the selected manuscript.
        With these additional member variables:
            .on_screen: True only if text from witness is visible on screen
            .first_imageid: id of the first *available* folio_image within the witness range. None if not found.
    '''
    ret = []
    if context['manuscript'] is not None and context['current_pair'] is not None:
        ret = context['manuscript'].get_witnesses()
        for witness in ret:
            if context['manuscript_views'].get_value() == 's':
                witness.on_screen = witness.contains_folio(
                    context['current_pair']['selected'])
            else:
                witness.on_screen = (
                    witness.contains_folio(
                        context['current_pair']['0']) or witness.contains_folio(
                        context['current_pair']['1']))
            witness.first_image = witness.get_first_available_folio_image()
    return ret


def get_image_pair_from_reference(reference, manuscript):
    if reference and not re.match('^\d+$', reference):
        # reference is alphnum, it is the slug of a version
        from models import Version, Witness, Folio_Image
        versions = Version.objects.filter(slug=reference.lower())
        if versions.count():
            witnesses = Witness.objects.filter(
                manuscript=manuscript, version=versions[0])
            if witnesses.count():
                image = witnesses[0].get_first_available_folio_image()
                if image:
                    reference = image.id
    ret = get_image_pair_from_imageid(reference, manuscript)
    return ret


def get_image_pair_from_imageid(imageid, manuscript):
    ''' returns a dictionary for the pair of images which contains the image with id [imageid] in manuscript [manuscript].
        returns a dic for the first pair in the MS if [imageid] was not found.
        returns a dic for the last pair in the MS if [imageid] = -1.
    '''
    ret = {
        '0': None,
        '1': None,
        'id': '',
        'label': '',
        'previousid': '',
        'nextid': '',
        'selected': None}
    if manuscript is not None:
        pairs = manuscript.get_double_pages()
        if len(pairs) > 0:
            if str(imageid) == '-1':
                # last pair
                found_index = len(pairs) - 1
            else:
                found_index = None
                i = 0
                for pair in pairs:
                    if str(imageid) == str(pair['id']) or \
                        (pair['0'] is not None and str(pair['0'].id) == str(imageid)) or \
                            (pair['1'] is not None and str(pair['1'].id) == str(imageid)):
                        found_index = i
                        break
                    i = i + 1
                if found_index is None:
                    # first pair
                    found_index = 0
            ret = pairs[found_index]
            ret['selected'] = ret['1']
            if (ret['selected'] is None) or (
                    ret['0'] is not None and str(ret['0'].id) == str(imageid)):
                ret['selected'] = ret['0']

            if found_index > 0:
                ret['previousid'] = pairs[found_index - 1]['id']
            else:
                ret['previousid'] = ''
            if found_index < (len(pairs) - 1):
                ret['nextid'] = pairs[found_index + 1]['id']
            else:
                ret['nextid'] = ''

    return ret


def text_index_view(request):
    from cch.page_filters.page_filters import Filter, FilterOption, get_az_filter_qs
    from models import Version, Work, Version_Language, Language
    context = {}

    # 1. ADD UI FILTERS

    # index type
    context['text_index_types'] = Filter('Type', 'tp', request, 'tab', ((
        'By text name', 'na'), ('By abbreviation', 'ab'), ('By category', 'ca'), ('By king', 'ki')))

    # language
    language = Filter('Language', 'lg', request, 'link-list')
    # TODO: cache this query
    FilterOption('Any', 0, language)
    for lang in Language.objects.extra(
            where=[r'''EXISTS (SELECT * FROM editions_version_language WHERE language_id = editions_language.id)''']).order_by('name'):
        if lang.id > 2:
            FilterOption(lang.name, lang.id, language)
    context['filter_language'] = language

    # 2. QUERY FORMULATION

    # Initial basic query
    filter_fields = []
    if context['text_index_types'].get_value() == 'ab':
        filter_fields = ['editions_version.standard_abbreviation']
        query_set = Version.objects.all()
    else:
        filter_fields = ['editions_version.name', 'editions_work.name']
        # trick to force the query set to do a join with the work table for us
        query_set = Version.objects.exclude(work__name__exact='NOTFOUND')

    # Filter by language
    if str(language.get_value()) != '0':
        query_set = query_set.filter(language__id=language.get_value())

    # Filter by a-z
    if context['text_index_types'].get_value() in ('na', 'ab'):
        context['a_to_z'] = get_az_filter_qs(request, query_set, filter_fields)
        letter = context['a_to_z'].get_value()
        query_set = query_set.extra(
            where=[
                get_concat_from_field_names(filter_fields) +
                " like %s"],
            params=[
                u'%s%%' %
                letter])

    # Grouping (text attribute / king)
    group_field_name = None
    if context['text_index_types'].get_value() in ('ca', 'ki'):
        group_field_name = 'group_name'
        # trick to force the query set to do a join with the work table for us
        query_set = query_set.exclude(work__name__exact='NOTFOUND')
        if context['text_index_types'].get_value() in ('ca',):
            query_set = query_set.extra(tables=['editions_text_attribute_work', 'editions_text_attribute'],
                                        where=['editions_work.id = editions_text_attribute_work.work_id',
                                               'editions_text_attribute_work.text_attribute_id = editions_text_attribute.id'],
                                        select={group_field_name: 'editions_text_attribute.name'})
        if context['text_index_types'].get_value() in ('ki',):
            query_set = query_set.extra(tables=['editions_king', 'editions_person'],
                                        where=['editions_work.king_id = editions_king.person_ptr_id',
                                               'editions_king.person_ptr_id = editions_person.id'],
                                        select={group_field_name: 'editions_person.name'})

    # Sort order
    # (we sort by the grouping field (e.g. king name) then by the order field (e.g. abbreviation))
    order_fields = []
    if group_field_name is not None:
        order_fields.append(group_field_name)
    order_fields.append('field_order')
    query_set = query_set.order_by().extra(
        select={
            'field_order': get_concat_from_field_names(filter_fields)},
        order_by=order_fields)

    # Grouping (2) - break the result set into groups
    if group_field_name is None:
        context['groups'] = [{'name': 'g1', 'records': query_set}]
    else:
        context['groups'] = []
        current_group = None
        for record in query_set:
            if current_group is None or current_group['name'] != record.group_name:
                current_group = {'name': record.group_name, 'records': []}
                context['groups'].append(current_group)
            current_group['records'].append(record)

    # Set version.odd = True/False on each version
    for group in context['groups']:
        odd = True
        for record in group['records']:
            record.odd = odd
            odd = not odd

    return get_template('website/text_index', context, request)


def search_view(request):
    from cch.logger.log_file import logp

    from cch.page_filters.page_filters import Filter, FilterOption
    from models import (Version, Work, Version_Language, Language, Edition,
                        King, Text_Attribute, Commentary, Witness)

    #logp.logTitle('start')

    context = {'st': request.REQUEST.get('st', '')}
    submitted = request.REQUEST.get('sm', False)
    reset_search = request.REQUEST.get('srt', False)

    # TODO: might need to be optimse as for the moment we are fecthing all the records in the result set
    # even if they are not shown on the current page.
    query_vars_to_ignore = ['page']

    # text types
    text_type = Filter(
        'Type of text',
        'tt',
        request,
        'link-list',
        (('Edition',
          'ed'),
         ('Commentary',
          'co'),
            ('Translation of an edition',
             'edtrl'),
            ('Transcription of a witness',
             'trc'),
            ('Translation of a witness',
             'trl')),
        query_vars_to_ignore=query_vars_to_ignore)
    context['filter_text_type'] = text_type

    # language
    language = Filter('Language', 'lg', request, 'link-list',
                      query_vars_to_ignore=query_vars_to_ignore)
    # TODO: cache this query
    FilterOption('Any', 0, language)
    #if text_type.get_value() in ['ed', 'trc']:
    if True:
        for lang in Language.objects.extra(
                where=[r'''EXISTS (SELECT * FROM editions_version_language WHERE language_id = editions_language.id)''']).order_by('name'):
            if lang.id > 2:
                FilterOption(lang.name, lang.id, language)
    context['filter_language'] = language

    # kings
    king = Filter('King', 'kg', request, 'link-list',
                  query_vars_to_ignore=query_vars_to_ignore)
    FilterOption('Any', 0, king)
    for aking in King.objects.all().order_by('name'):
        FilterOption(aking.name, aking.id, king)
    context['filter_king'] = king

    # text categories
    category = Filter('Category', 'ct', request, 'link-list',
                      query_vars_to_ignore=query_vars_to_ignore)
    FilterOption('Any', 0, category)
    for acategory in Text_Attribute.objects.all().order_by('name'):
        FilterOption(acategory.name, acategory.id, category)
    context['filter_category'] = category

    context['items'] = []

    if text_type.get_value() in ['ed', 'edtrl', 'co']:
        context['item_type'] = 'edition'
        result_model = Edition
    else:
        context['item_type'] = 'witness'
        result_model = Witness

    result_model.get_snippet = get_snippet

    ''' Overview of the search process:
        * first apply the selected filters (lg, king, text attribute) with a Django queryset on the DB
        * if user typed keywords:
            * run the search with Whoosh
            * intersect the whoosh results with the queryset
            * only keep the result items which have some textual content for the selected type of text
            * generate snippets (either whoosh highlight or truncated excerpt from the beginning)
        * otherwise
            * sort the result set
            * only keep the result items which have some textual content for the selected type of text
            * generate snippets
    '''

    #logp.log('pre filter')

    filtered_items = None
    if str(language.get_value()) + str(king.get_value()) + \
            str(category.get_value()) != '000' or not context['st']:
        filtered_items = result_model.objects.all()
    if context['item_type'] == 'edition':
        # apply the filters
        # these results will be used by the text search or the non-text search
        if str(language.get_value()) != '0':
            filtered_items = filtered_items.filter(
                version__language__id=language.get_value())
        if str(king.get_value()) != '0':
            filtered_items = filtered_items.filter(
                version__work__king__id=king.get_value())
        if str(category.get_value()) != '0':
            filtered_items = filtered_items.filter(
                version__work__text_attribute__id=category.get_value())
    if context['item_type'] == 'witness':
        # apply the filters
        # these results will be used by the text search or the non-text search
        if str(language.get_value()) != '0':
            filtered_items = filtered_items.filter(
                language__id=language.get_value())
        if str(king.get_value()) != '0':
            filtered_items = filtered_items.filter(
                work__king__id=king.get_value())
        if str(category.get_value()) != '0':
            filtered_items = filtered_items.filter(
                work__text_attribute__id=category.get_value())

    #logp.log('mid')

    # text search
    searcher = None
    if context['st']:
        from whoosh.qparser import QueryParser, MultifieldParser
        from whoosh.index import open_dir

        import sys
        import os

        ix = open_dir(
            os.path.join(
                settings.PROJECT_FILEPATH,
                'indices'),
            context['item_type'])
        searcher = ix.searcher()

        if context['item_type'] == 'edition':
            text_field_names = {
                'ed': 'text',
                'edtrl': 'translation',
                'co': 'commentary'}
            text_field_name = text_field_names[text_type.get_value()]
            query = MultifieldParser([text_field_name,
                                      'title',
                                      'abbreviation',
                                      'editors',
                                      'attributes'],
                                     ix.schema,
                                     {text_field_name: 1.0,
                                      'title': 5.0,
                                      'abbreviation': 3.0,
                                      'editors': 1.0,
                                      'attributes': 3.0}).parse(context['st'])
            result_model = Edition

        if context['item_type'] == 'witness':
            text_field_names = {'trl': 'translation', 'trc': 'transcription'}
            text_field_name = text_field_names[text_type.get_value()]
            query = MultifieldParser([text_field_name, 'title', 'editors', 'attributes', 'work_name'],
                                     ix.schema,
                                     {text_field_name: 1.0,
                                      'title': 5.0,
                                      'editors': 1.0,
                                      'attributes': 3.0,
                                      'work_name': 5.0}).parse(context['st'])

        #logp.log('post filtering 1')

        results = searcher.search(query, limit=None)
        resultids = [result['recid'] for result in results]
        filtered_items_dict = {}
        if filtered_items is None:
            filtered_items_dict = result_model.objects.in_bulk(resultids)
        else:
            for e in filtered_items:
                filtered_items_dict[e.id] = e

        #logp.log('post filtering 2')

        for i in range(0, len(resultids)):
            # we get a weird error message if we simply pass the whoosh result item (i.e Hit object)
            # and then read its fields from the template.
            # So we have to copy the fields one by one.
            if int(resultids[i]) in filtered_items_dict:
                #logp.log(''+resultids[i])
                item = filtered_items_dict[int(resultids[i])]
                item.snippet_field_name = text_field_name
                item.whoosh = results[i]
                # this function call is very slow. Approx 1 sec for 15 items.
                #item.snippet = results[i].highlights(text_field_name, top=3)
                #item.snippet = get_snippet(results[i][text_field_name])
                #if item.snippet is None or len(item.snippet) == 0:
                #    item.snippet = get_snippet_from_text(results[i][text_field_name])
                if True or len(item.whoosh[text_field_name]) > 10:
                    context['items'].append(item)

    else:
        # no-text search

        # sort
        if context['item_type'] == 'edition':
            items = [
                edition for edition in filtered_items.order_by('abbreviation')]
        if context['item_type'] == 'witness':
            items = [
                edition for edition in filtered_items.order_by('manuscript__sigla')]
        context['items'] = []

        # create the snippets from the first words in the edition/translation
        for item in items:
            text = ''
            if text_type.get_value() in ['ed']:
                text = item.text
            if text_type.get_value() in ['edtrl']:
                if item.edition_translation and item.edition_translation.text:
                    text = item.edition_translation.text
            if text_type.get_value() in ['co']:
                text = ''.join([commentary.text for commentary in Commentary.objects.filter(
                    edition=item, sort_order=1)])
            if text_type.get_value() in ['trc']:
                if item.witness_transcription and item.witness_transcription.text:
                    text = item.witness_transcription.text
            if text_type.get_value() in ['trl']:
                if item.witness_transcription and item.witness_transcription.witness_translation and item.witness_transcription.witness_translation.text:
                    text = item.witness_transcription.witness_translation.text

            item.snippet_marked_up = text

            if True or len(item.snippet_marked_up) > 10:
                context['items'].append(item)

    context['result_size'] = len(context['items'])

    #logp.log('render')

    ret = get_template('website/search', context, request)

    if searcher:
        searcher.close()

    #logp.log('end')

    return ret


def get_snippet(self):
    ret = ''
    from cch.logger.log_file import logp

    from django.utils.html import strip_tags
    snippet_field_name = getattr(self, 'snippet_field_name', '')
    to_truncate = None
    if snippet_field_name:
        # let Whoosh produce the highlights from the whoosh plain text field
        #logp.log('h1')
        # !!! This function takes a lot of time.
        # Even when it does not find any occurences in the text.
        # Changing top to 2 won't change a lot.
        ret = self.whoosh.highlights(snippet_field_name, top=3)
        if not ret:
            to_truncate = self.whoosh[snippet_field_name]
    else:
        #logp.log('h2')
        to_truncate = re.sub(r'\[[^]]*\]', '', self.snippet_marked_up)
        to_truncate = strip_tags(to_truncate)
    if to_truncate:
        #logp.log('h3')
        # custom snippet greneration from marked-up text
        ret = get_snippet_from_text(to_truncate)
    return ret


def get_snippet_from_text(text, length=15):
    if text is None:
        return ''
    ret = text.strip()
    if len(ret) > 0:
        #from django.utils.html import strip_tags
        from django.utils.text import truncate_words
        #ret = strip_tags(text)
        ret = truncate_words(ret, length)
    return ret
