'''
$Id: views.py 50 2010-10-12 15:05:59Z goffer.looney@gmail.com $
'''
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django import http, template

# TODO: move to self-contained module
@staff_member_required
def view_categories(request):
    from django.template.context import Context
    
    context = {}
    
    from models import Global_Var_Category
    context['categories'] = Global_Var_Category.objects.all().order_by('name')
    
    template_name = 'categories'
    return render_to_response('gsettings/%s.html' % template_name, Context(context), context_instance=template.RequestContext(request)) 

@staff_member_required
def view_category(request, categoryid):
    from django.template.context import Context
    from models import Global_Var
    
    context = {}
    
    context['vars'] = Global_Var.objects.filter(global_var_category__id = categoryid).order_by('name')

    if request.POST is not None and '_save' in request.POST:
        context['submitted'] = True
        from gsettings.context_processor import _get_vars_as_context
        from gsettings.gvars import __get_cast_var
        # submit all the variables
        for var in context['vars']:
            varid = 'v%s' % var.id
            if varid in request.POST:
                var.value = request.POST[varid]
                try:
                    __get_cast_var(var)
                    var.save()
                except Exception, e:
                    context['errors'] = True
                    var.error_message = 'Invalid format'
                    
    from models import Global_Var_Category
    context['category'] = Global_Var_Category.objects.get(id=categoryid)
    
    template_name = 'category'
    return render_to_response('gsettings/%s.html' % template_name, Context(context), context_instance=template.RequestContext(request)) 
