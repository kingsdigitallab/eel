'''
$Id: context_processor.py 44 2010-10-11 11:24:33Z goffer.looney@gmail.com $
'''

from django.conf import settings

def _get_vars_as_context():
    ''' Dump all the settings variables into a dictionary and return it '''
    ret = {}
    from gvars import __get_vars
    vars = __get_vars()
    if vars is not None:
        # convert the cache into a structured context variable
        for var_name in vars:
            for category_name in vars[var_name]:
                if category_name not in ret: ret[category_name] = {}
                ret[category_name][var_name] = vars[var_name][category_name]
    
    return ret  

def all_gvars(request):
    return {
            'gsettings': _get_vars_as_context(), 
            }
