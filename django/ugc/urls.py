'''
$Id: urls.py 2 2010-08-11 11:17:12Z goffer.looney@gmail.com $
'''
from django.conf.urls.defaults import *
from django.contrib import admin
import views

# /? in the pattern is necessary. We need to capture the / as well. 
# Otherwise registration app will capture them instead.

urlpatterns = patterns('',
    (r'^login/?$',          views.login_view),
    (r'^logout/?$',         views.logout_view),
    #(r'^directory/?$',      views.directory_view),
    #(r'^dashboard/?',       views.dashboard_view),
    (r'^terms/?',           views.terms_view),
    (r'^reset-password/?',  views.reset_password_view),
    (r'^/?$',               views.profile_view),
)
