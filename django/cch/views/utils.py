from django import http, template
from django.shortcuts import render_to_response
from django.template.context import Context
import re
import htmlentitydefs


def get_concat_from_field_names(field_names):
    ret = 'concat(%s)' % ', '.join(field_names)
    return ret


def get_template(path, context, request):
    return render_to_response(path + '.html', Context(context),
                              context_instance=template.RequestContext(request))


def get_json_response(python_dict):
    import simplejson as json
    from django.http import HttpResponse
#    from django.utils.safestring import mark_safe
#    context = Context({'response': mark_safe(u'(%s)' % json.dumps(python_dict))})
#    response = render_to_response('admin/json/search.html', context, context_instance=template.RequestContext(request))
#    response['Cache-Control'] = 'public, no-cache'
#    response['Content-Type'] = 'application/x-javascript; charset=utf-8'
    response = HttpResponse(
        u'(%s)' %
        json.dumps(python_dict),
        None,
        None,
        'application/x-javascript; charset=utf-8')
    response['Cache-Control'] = 'public, no-cache'
    return response


def get_file_response(download_filename, filepath):
    from django.http import HttpResponse

    content = open(filepath, 'rb')

    # generate the file
    response = HttpResponse(
        content,
        content_type='application/zip'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % download_filename
    return response


def removetree(path):
    import os

    if os.path.exists(path):
        path = os.path.abspath(path)
        # make sure we don't delete root folders...
        assert(len(path) > 3)
        import shutil
        shutil.rmtree(path)


def get_request_var(request, key, default=''):
    ret = request.GET.get(key, '').strip()
    if ret == '':
        ret = default
    return ret

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
#
# October 28, 2006 | Fredrik Lundh
# http://effbot.org/zone/re-sub.htm#unescape-html
#


def decodeHtmlEntities(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def write_file(file_path, content, encoding='utf8'):
    f = open(file_path, 'wb')
    if encoding:
        content = content.encode(encoding)
    f.write(content)
    f.close()
