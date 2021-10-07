from django.conf.urls.defaults import *
import settings
from editions import admin_views
from editions import text_views
from editions import website_views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.static import serve
import ugc.views

admin.autodiscover()

# LOGS
# this should go into the setting.py or django.wsgi file
# but it fails to import log when I do so
from .cch.logger.log_file import log
if not settings.DEBUG:
    log.setLevel(-1)

# PREFIXES
prefix = settings.DJANGO_WEBPATH_PREFIX
#user_prefix = settings.DJANGO_WEBPATH_PREFIX_MEMBERS

# DB MAINTENANCE
backend_mantenance_url = prefix + 'admin'
if not settings.DB_MAINTENANCE:
    backend_mantenance_url += '/maintenance.html'

frontend_mantenance_url = ''
if not settings.FRONTEND_MAINTENANCE:
    frontend_mantenance_url = prefix + 'maintenance.html'

# HTTP EXPIRY


def expire_static_serve(*args, **kwargs):
    from django.views.static import serve
    response = serve(*args, **kwargs)
    if settings.ADMIN_INCLUDE_CACHE != 0:
        response['Cache-Control'] = 'max-age=%s, must-revalidate' % settings.ADMIN_INCLUDE_CACHE
    else:
        response['Cache-Control'] = 'no-cache, must-revalidate'
    return response


handler500 = 'editions.500_view.server_error'

urlpatterns = patterns(
    '',
    # (r'test/?$', website_views.test_view),

    (r'^' + backend_mantenance_url, admin_views.maintenance),

    (r'^' + prefix + 'admin/gsettings/edit/',
     include('gsettings.urls')),

    (r'/bulk_edit/?$', admin_views.bulk_edit),

    # --------- BACK END -----------
    #(r'^'+prefix+'accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/media/website/_a/i/favicon.ico'}),

    (r'^' + prefix + 'admin/', include('editions.urls_admin')),

    (r'^' + prefix + 'admin/', include(admin.site.urls)),

    (r'^tinymce/', include('tinymce.urls')),
    (r'^' + prefix + 'db/admin/json/search$',
     admin_views.json_search),

    # --------- FRONT END -----------

    (r'^' + prefix + 'user/', include('ugc.urls')),
    (r'^' + prefix, include('editions.urls')),

    # media (NOT used on stg or production server; only for the django manage
    # runserver)
    (r'^media/(?P<path>.*)$', expire_static_serve,
        {'document_root': settings.MEDIA_ROOT}),

    (r'^' + prefix + 'blog(/?)$', website_views.blog_view),

    # PROXY - to djatoka
    # note that this should be set up with Apache on the
    # staging/live server
    (r'^' + prefix + '(?P<url>adore-djatoka.*)$',
     'httpproxy.views.proxy'),
    # floating folder for iipviewer assets
    (r'(?P<path>zoomer/.*)$', serve,
     {'document_root': settings.WEBSITE_ROOT}),

    (r'^' + settings.DJANGO_WEBPATH_PREFIX_MEMBERS,
     include('registration.backends.default.urls')),

    # DJANGO CMS
    (r'^(index.html)/?$', website_views.xmod_redirect_view),
    (r'^(' + prefix + '.*)/([^/]+)\.html/?$',
     website_views.xmod_redirect_view),
    (r'^' + prefix + '', include('cms.urls')),
)
