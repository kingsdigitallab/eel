# -*- coding: utf-8 -*-
# $Id: tags_filters.py 641 2010-10-15 13:38:47Z gnoel $

from django import template
import urllib

register = template.Library()

@register.simple_tag
def record_list(records, field_name, separator):
    ret = []
    #print records.__class__
    #print dir(records)
    for record in records.all().order_by('id'):
        ret.append(str(getattr(record, field_name)))
    return separator.join(ret) 

@register.simple_tag
def updated_query_string(request, akey=None, aval=None):
    '''  Returns the quey string '?a=b&c=d' where akey has been set to aval.
         If akey is None, the query original query string is returned
         If aval is None, the akey parameter is removed from the query string 
    '''
    req = dict(request.GET.items())
    if akey is not None:
        req[akey] = aval
    else:
        if aval is None and akey in req:
            del req[akey]
    ret = '?' + urllib.urlencode(req)
    return ret
