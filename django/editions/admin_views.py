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
from cch.views.utils import get_json_response
from xml.dom import minidom
#log.log(text, 2)
from cch.logger.log_file import log
import htmlentitydefs

from django.http import HttpResponse, Http404

@staff_member_required
def media(request, path=None):
    return HttpResponse('test:'+path)

@staff_member_required
def editions(request, url):
    url = url.rstrip('/') # Trim trailing slash, if it exists.
    admin.site.root_path = re.sub(re.escape(url) + '$', '', request.path)
    return app_index(request, url)

@staff_member_required
def bulk_edit(request, url=None):
    context = {}
    context['folios'] = Folio_Image.objects.filter(id__in=request.GET.get('ids', '').split(',')).order_by('batch', 'path', 'filename_sort_order')
    context['folio_sides'] = Folio_Side.objects.filter().order_by('id')
    context['manuscripts'] = Manuscript.objects.all().order_by('archive__city', 'archive__name')
    context['show_thumbnails'] = request.POST.get('thumbnails_set', 0)
    
    manuscript = Manuscript.objects.get(id=request.POST.get('manuscript', '1'))
    
    page = request.POST.get('page_number', '').strip()
    if page != '':
        page = int(page)
        
    folio_number = request.POST.get('folio_number', '').strip()
    if folio_number != '':
        folio_number = int(folio_number)
    folio_side = Folio_Side.objects.get(id=request.POST.get('folio_side', '1'))
    folio_sides = {}
    for s in Folio_Side.objects.all():
        folio_sides[s.id] = s
    recto = Folio_Side.objects.get(id=3)
    verso = Folio_Side.objects.get(id=4)
    unspecified_side = Folio_Side.objects.get(id=1)
    
    action = request.POST.get('action', '').strip()

    #if action == 'operations':

    
    if len(action):
        for folio in context['folios']:
            modified = False
            
            if action == 'operations':
                number = re.findall(r'(?i)0*(\d{1,3})\D*$', folio.filename)
                if str(request.POST.get('manuscript_set', '0')) == '1':
                    folio.manuscript = manuscript
                    modified = True
                if str(request.POST.get('page_set', '0')) == '1':
                    folio.page = page
                    if page != '':
                        page = page + 1
                    modified = True
                if str(request.POST.get('folio_set', '0')) == '1':
                    folio.folio_number = folio_number
                    if folio_number != '' and folio_side == verso:
                        folio_number = folio_number + 1
                    folio.folio_side = folio_side
                    if folio_side == recto: 
                        folio_side = verso
                    elif folio_side == verso:
                        folio_side = recto
                    modified = True
                if str(request.POST.get('folio_number_set', '0')) == '1':
                    if len(number) > 0:
                        folio.folio_number = number[0]
                    else:
                        folio.folio_number = ''
                    modified = True
                if str(request.POST.get('folio_side_set', '0')) == '1':
                    if re.search('(?i)[^a-z]r$', folio.filename): 
                        folio.folio_side = recto
                    elif re.search('(?i)[^a-z]v$', folio.filename): 
                        folio.folio_side = verso
                    else: 
                        folio.folio_side = recto
                        #folio.folio_side = unspecified_side
                    modified = True
                if str(request.POST.get('page_number_set', '0')) == '1':
                    if len(number) > 0:
                        folio.page = number[0]
                    else:
                        folio.page = ''
                    modified = True
                if str(request.POST.get('archived_set', '0')) == '1':
                    folio.archived = True
                    modified = True
                if str(request.POST.get('unarchived_set', '0')) == '1':
                    folio.archived = False
                    modified = True
            
            if action == 'change_values':

                '''
                        <input class="txt-folio-number" type="text" name="fn-{{folio.id}}" value="{{folio.folio_number}}" />
                        <input type="radio" id="fs-{{folio.id}}-id" name="fs-{{folio.id}}" {% ifequal folio.folio_side.id side.id %}checked="checked"{% endifequal %} >
                        <input class="txt-folio-number" type="text" name="pn-{{folio.id}}" value="{{folio.page}}" />
                        <input type="checkbox" name="arch-{{folio.id}}" {% if folio.archived %}checked="checked"{% endif %} />
                        <textarea class="txta-folio-note" name="inotes-{{folio.id}}">{{ folio.internal_notes }}</textarea>
                '''                
                
                folio.folio_number = request.POST.get('fn-%s' % (folio.id,), '')
                folio.folio_side = folio_sides[int(request.POST.get('fs-%s' % (folio.id,), 1))]
                folio.page = request.POST.get('pn-%s' % (folio.id,), '')
                folio.archived = (len(request.POST.get('arch-%s' % (folio.id,), '')) > 0)
                folio.internal_notes = request.POST.get('inotes-%s' % (folio.id,), '')
                modified = True            
            
            if modified: folio.save()

            
    return view_utils.get_template('admin/editions/folio_image/bulk_edit', context, request)

# This method is mostly copied from [PYTHON]\Lib\site-packages\django\contrib\admin\sites.py, app_index()
# It splits all the tables into groups, the name of the group they belong to is determined by the "table_group" variable in the models
# It uses the existing application templates ([PYTHON]\Lib\site-packages\django\contrib\admin\templates\admin\app_index.html)
# No need to exend that template
# TODO: move this to another module and reuse it
def app_index(request, app_label, extra_context=None):
    user = request.user
    has_module_perms = user.has_module_perms(app_label)
    app_list = {}
    app_dict = {}
    for model, model_admin in admin.site._registry.items():
        if app_label == model._meta.app_label:
            if has_module_perms:
                perms = {
                    'add': user.has_perm("%s.%s" % (app_label, model._meta.get_add_permission())),
                    'change': user.has_perm("%s.%s" % (app_label, model._meta.get_change_permission())),
                    'delete': user.has_perm("%s.%s" % (app_label, model._meta.get_delete_permission())),
                }
                # GN - use the table group as an index for the app
                try:
                    app_index = model.table_group
                except AttributeError:
                    app_index = ''
                
                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'admin_url': '%s/' % model.__name__.lower(),
                        'perms': perms,
                        #'reference': model.reference_table,
                    }
                    if (app_index in app_list):
                        app_list[app_index]['models'].append(model_dict),
                    else:
                        # First time around, now that we know there's
                        # something to display, add in the necessary meta
                        # information.
                        app_list[app_index] = {
                            'name': app_label.title(),
                            'app_url': '',
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }
                        if (app_index != ''):
                            app_list[app_index]['name'] += ' - ' + app_index
                        #app_list.append(app_dict)    
    #if not app_dict:
    #    raise http.Http404('The requested admin page does not exist.')
    # Sort the models alphabetically within each app.
    app_list_final = []
    for group_name, app in app_list.items():
        app['models'].sort(lambda x, y: cmp(x['name'], y['name']))
        app_list_final.append(app)
    context = {
        'title': _('%s administration') % capfirst(app_label),
        #'app_list': [app_dict],
        'app_list': app_list_final,
        'root_path': admin.site.root_path,
    }
    context.update(extra_context or {})
    return render_to_response(admin.site.app_index_template or 'admin/app_index.html', context,
        context_instance=template.RequestContext(request)
    )

def maintenance(request):
    from django.template.context import Context
    return render_to_response('admin/maintenance.html', Context({}), context_instance=template.RequestContext(request))

# TODO: move to cch
def json_search(request):
    '''    Request: http://localhost:8000/db/admin/json/search?limit=10&model=bibliographic_entry&q=b
        Parameters:
            limit:    max size of the result set                 [default=100]
            model:    name of the model we are searching in     [MANDATORY]
            q:        search phrase                            [default='']
            fmt:    format of the result set                [default='ref']
                    ref: the second element will be get_reference_name()
                    rpr: the second eleemnt will be the representation (i.e. unicode())
            
    '''
    query_string = getQueryStringParams(request)
    
    #json_list = ur'''({'error': '', 'content_type': 0, 'records': []})''';
    json_list = {'error': '', 'content_type': 0, 'records': []}
    
    # TODO: ERROR MANAGEMENT

    try:
        if ('model' in query_string):
            # 1. run the query with ChangeList item, just like Django admin does it in the change list view page
            model_name = query_string['model']
            request_copy = request
            # save the get from the request and replace it with a copy which doesn't contain the 'model' param
            get_saved = request.GET
            get_pc = request.GET.copy()
            request.GET = get_pc
            del request.GET['model']
            limit = 100
            # remove our own parameters so ChangeList doesn't raise an exception
            if 'search' in request.GET: del request.GET['search']
            if 'limit' in request.GET:
                limit = int(request.GET['limit'])
                del request.GET['limit']
            get_reference = True
            if 'fmt' in request.GET:
                if (request.GET['fmt'] == 'rpr'): get_reference = False
                del request.GET['fmt']
            
            query = ''
            result = None
            ma = getModelAdminFromModelName(model_name)
            if 'q' in request.GET:
                query = request.GET['q']
            if len(query) > 0:
                from django.contrib.admin.views.main import ChangeList, ERROR_FLAG
                cl = None
                # only neede for django 1.0, not 1.1 
                # import admin
                cl = ChangeList(request, ma.model, ma.list_display, ma.list_display_links, ma.list_filter,
                    ma.date_hierarchy, ma.search_fields, ma.list_select_related, ma.list_per_page, ma.list_editable, ma)
                result = cl.result_list
            else:
                result = ma.model.objects.order_by('-id')
            # 2. convert the result to JSON
            ''' 
                {'content_type': 115, 'records': [[6, 'Jose Cabrujas', 'Cabrujas, Jose (17-07-1937)'],[5, 'Jose Triana', 'Triana, Jose']]}
            '''
            #json_list = ''
            content_typeid = get_content_typeid_from_model_name(model_name)
            size = 0

            for record in result:
                size += 1
                if size > limit:
                    break
                #if json_list != '': json_list += ','
                if get_reference:
                    short_name = record.get_reference_name()
                else:
                    short_name = record.__unicode__()
                json_list['records'].append((record.id, short_name.replace('\'', '\\\''), record.get_list_name().replace('\'', '\\\'')))
            
            #json_list = ur"({'error':'','content_type':%d,'model':'%s','records':[%s]})" % (content_typeid, model_name, json_list)
            #json_list = ur"{'error':'','content_type':%d,'model':'%s','records':[%s]}" % (content_typeid, model_name, json_list)
            json_list['content_type'] = content_typeid
            json_list['model'] = model_name
            
            # restore the original GET var in the request 
            request.GET = get_saved
    except:
        #raise
        import sys
        #json_list = ur'''({'error': '%s', 'content_type': 0, 'records': []})''' % str(sys.exc_info()[1]).replace('\'', '\\\'')
        json_list['error'] = str(sys.exc_info()[1]).replace('\'', '\\\'')
    
    #return get_json_response({'error':'','content_type':69,'model':'person','records':[[4,'Geoffroy','Geoffroy'],[3,'Edgar','Edgar'],[2,'Alfred','Alfred'],[1,'Cnut','Cnut']]})
    return get_json_response(json_list)
    
    from django.template.context import Context
    from django.utils.safestring import mark_safe
    context = Context({'response': mark_safe(json_list)})
    response = render_to_response('admin/json/search.html', context, context_instance=template.RequestContext(request))
    response['Cache-Control'] = 'public, no-cache'
    response['Content-Type'] = 'application/x-javascript; charset=utf-8'

    return response
    
# TODO: move to cch
def getQueryStringParams(request):
    return dict(request.GET.items())

# TODO: move to cch
def getModelAdminFromModelName(model_name):
    from django.db import models
    from django.contrib.admin.sites import site
    # TODO: generalise
    app_label = 'editions'
    model = models.get_model(app_label, model_name)
    if model is None:
        raise http.Http404("App %r, model %r, not found." % (app_label, model_name))
    try:
        admin_obj = site._registry[model]
    except KeyError:
        raise http.Http404("This model exists but has not been registered with the admin site.")
    return admin_obj

def get_content_typeid_from_model_name(model_name):
    from django.contrib.contenttypes.models import ContentType
    # TODO: generalise
    content_type = ContentType.objects.get(app_label='editions', model=model_name)
    return content_type.id

