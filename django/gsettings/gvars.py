'''
$Id: gvars.py 44 2010-10-11 11:24:33Z goffer.looney@gmail.com $
'''

from datetime import datetime, date
from models import Global_Var
from django.conf import settings
from django.core.cache import cache

'''  see gsettings.models.Global_Var_Type '''
VAR_TYPE_STRING     = 1
VAR_TYPE_INT        = 2
VAR_TYPE_FLOAT      = 3
VAR_TYPE_DATETIME   = 4
VAR_TYPE_DATE       = 5

def get_value(name, category_name=None):
    ''' Returns the value of a variable from the cache, or the database if the cache is empty/expired/disabled.
        Returns None if variable is not found.
    '''
    ret = None
    vars = __get_vars_from_cache()
    if vars is not None:
        if name in vars:
            ret = vars[name]
            if category_name is None:
                # pick the first category
                for i in ret:
                    ret = ret[i]
                    break
            else:
                if category_name in ret:
                    ret = ret[category_name]
    else:
        ret = get_value_db(name, category_name)
    return ret

def get_value_db(name, category_name=None):
    ''' Returns the value of a variable from the database.
        Never tries the cache.  
        Returns None if the variable is not found.'''
    ret = None
    var = Global_Var.objects.filter(name=name)
    if category_name is not None:
        var = var.filter(global_var_category__name=category_name)
    if var.count():
        var = var[0]
        ret = __get_cast_var(var)
    return ret

def cache_values(force_reload = False):
    raise Exception('cache_values() is deprecated. GSettings caching uses your projects cache settings (see CACHE_BACKEND)')

''' --------------- INTERNAL FUNCTIONS -------------- '''

def __get_vars():
    ''' Returns a dictionary with all the gsettings variable values.
        Variables are read from the cache (if caching is enabled AND cache is not empty AND not expired)
        or the database (otherwise).
        Repopulate the cache if necessary.
    '''
    ret = __get_vars_from_cache()
    if ret is None: ret = __get_vars_from_db()
    return ret

def __get_vars_from_cache():
    ''' Returns a dictionary with all the gsettings variable values.
        Variables are read from the cache. If the cache is expired or empty, read from the DB and fill the cache.
        If caching is disabled, returns None.
    '''
    ret = None
    if __is_cache_enabled():
        ret = cache.get('gsettings.vars', None)
        if ret is None:
            # get all the data from the DB to a dictionary
            ret = __get_vars_from_db()
            timeout = getattr(settings, 'GSETTINGS_CACHE_TIMEOUT', None)
            cache.set('gsettings.vars', ret, timeout)
    return ret

def __get_vars_from_db():
    ''' Returns a dictionary with all the gsettings variable values.
        Variables are read from the database. It neither read from nor write to the cache.
    '''
    ret = {}
    for var in Global_Var.objects.all():
        if var.name not in ret:
            ret[var.name] = {}
        ret[var.name][var.global_var_category.name] = __get_cast_var(var)
    return ret
    
def __get_cast_var(var):
    ''' Returns the value of a variable. it is cast into the proper python type. '''
    return __get_cast_value(var.value, var.global_var_type.id)
    
def __get_cast_value(value, typeid):
    ''' Returns the value of a variable. it is cast into the proper python type. '''
    ret = value
    try:
        if typeid == VAR_TYPE_INT: ret = int(ret)
        if typeid == VAR_TYPE_FLOAT: ret = float(ret)
        if typeid == VAR_TYPE_DATE:
            parts = ret.split('-')
            ret = date(int(parts[0]), int(parts[1]), int(parts[2]))
        if typeid == VAR_TYPE_DATETIME:

            parts = ret.split(' ')
            parts_date = parts[0].split('-') 
            parts_time = parts[1].split(':') 
            ret = datetime(int(parts_date[0]), int(parts_date[1]), int(parts_date[2]), int(parts_time[0]), int(parts_time[1]), int(parts_time[2]))
    except:
        raise ValueError('Invalid format.')
    return ret
    
def __get_string_from_value(value):
    ''' Returns a string from a python value. 
        The format of this string is compatible with database format for global variables. '''
    ret = value
    type_name = value.__class__.__name__
    if type_name == 'int':
        str(ret)
    if type_name == 'float':
        str(ret)
    if type_name == 'date':
        ret.__str__()
    if type_name == 'datetime':
        ret.__str__()
    return ret

def __is_cache_enabled():
    ''' Returns  True if caching is enabled in the project settings. '''
    return (getattr(settings, 'CACHE_BACKEND', None) is not None)

#''' --------------- CACHING -------------- '''
#from django.core.signals import request_started
#
#def __on_request_started(sender, **kwargs):
#    # Clear the existing cache so if the database has been modified
#    # by a previous request we don't return stale values.
##    global cache
##    cache = None
##    print 'cache = None'
##    from django.conf import settings
##    if getattr(settings, 'GSETTINGS_AUTO_CACHE', False):
##        cache_values()
#    pass
#
#request_started.connect(__on_request_started)
