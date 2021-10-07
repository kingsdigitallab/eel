'''
$Id: urls.py 2 2010-08-11 11:17:12Z goffer.looney@gmail.com $
'''
from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
    # Example:
    # (r'^djtest/', include('djtest.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    (r'^$', 'gsettings.views.view_categories'),
    (r'^(?P<categoryid>\d+)/$', 'gsettings.views.view_category'),
)
