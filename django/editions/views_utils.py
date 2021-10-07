from cch.views.utils import get_template, get_json_response

def get_page_not_found(request, url=''):
    from django.http import HttpResponseNotFound
    return (HttpResponseNotFound)(get_template('404', {}, request))

