# Author: geoffroy.noel@kcl.ac.uk
# This is a completely generic apache-wsgi configuration file (no project-specific constants here)
# If you place this file under [MY_DJANGO_SITE]/apache/django.wsgi, 
# it will automatically add the project to the python path and make sure the project is enabled 
import os, sys
prj_path = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath( __file__ )), '..'))
prj_parent_path = os.path.normpath(os.path.join(prj_path, '..'))
module_name = os.path.basename(prj_path)

def add_path(p): 
	if p not in sys.path: sys.path.append(p)
add_path(prj_parent_path)
add_path(prj_path)

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % module_name
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

#from ootw.debug import log
#log.logTitle('WSGI RELOADED')
