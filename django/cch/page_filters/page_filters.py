# $Id: page_filters.py 665 2011-11-23 22:52:32Z gnoel $
"""
    A page filters manages a parameter in the URL query string.
    It can represent a:
        filter with multiple options for a form (checkbox, list of links)
        series of tabs
        menu
        list of columns in a table
    It contains multiple options. Each option correspond to a distinct value.  
"""

# Base classes, each filter is linked to a parameter in the query string and each option to a value 

class Filter(object):
    """ A filter, e.g. pagination """ 
    def __init__(self, label, varname, request, input_type='link', options=None, query_vars_to_ignore=[]):
        self.input_parameter = None
        self.label = label
        self.varname = varname
        self.request = request
        self.options = []
        self.input_type = input_type
        self.get_selected_option_cache = None
        self.default_option = None
        self.query_vars_to_ignore = query_vars_to_ignore
        if options is not None:
            self.add_options(options)
    def add_filter_option(self, option):
        ''' Add a single option.
        option is a FilterOption object '''
        self.options.append(option)
        self.get_selected_option_cache = None
    def add_options(self, options):
        ''' Add many filter option at once. 
        options is a sequence. For each item, option[0] is the label, option[1] is the value'''
        for option in options:
            self.add_option(option)
    def add_option(self, option):
        ''' Add a single option. 
        option[0] is the label, option[1] is the value'''
        return FilterOption(option[0], option[1], self)
    def get_selected_option(self, multiple=False):
        if self.get_selected_option_cache is None:
            self.get_selected_option_cache = self.__get_selected_option()
        ret = self.get_selected_option_cache
        if not multiple:
            if len(ret) > 0:
                ret = ret[0]
            else:
                ret = ''
        return ret
    def __get_default_option(self):
        '''  Returns the default option. If disabled, returns the first enabled option. '''
        if self.default_option is not None and not self.default_option.disabled:
            return self.default_option
        ret = self.options[0]
        for option in self.options:
            if not option.disabled:
                return option
        return ret
    def set_default_option(self, valname=None):
        ''' sets the deault option, if not found set to None. '''
        self.default_option = None
        if valname is not None:
            for option in self.options:
                if (u'%s' % option.valname) == (u'%s' % valname):
                    self.default_option = option
                    break
    def has_multiple_options(self):
        return len(self.options) > 1
    def get_value(self):
        return (self.get_selected_option()).valname
    def __get_selected_option(self):
        input = self.get_input_parameter()
        ret = []
        for option in self.options:
            if (option.valname in input) and (not option.disabled): ret.append(option)
        if len(ret) == 0: ret.append(self.__get_default_option())
        return ret
    def get_input_parameter(self):
        if self.input_parameter is not None: return self.input_parameter
        return self.get_input_parameter_internal()
    def get_input_parameter_internal(self):
        return get_request_var(self.request, self.varname, [], True)
    def set_input_parameter(self, input_parameter=None):
        ''' [input_parameter] can be a tuple/list or a string '''
        self.get_selected_option_cache = None
        if input_parameter is not None and isinstance(input_parameter, basestring):
            input_parameter = [input_parameter]
        self.input_parameter = input_parameter        

class FilterOption(object):
    """ One option in a filter e.g.: A to Z """
    def __init__(self, label, valname, filter, disabled=False):
        self.label = label
        self.valname = '%s' % valname
        self.filter = filter
        self.filter.add_filter_option(self)
        self.disabled = disabled
    def selected(self):
        return (self in self.filter.get_selected_option(True))
    def query_string(self):
        # return a non-safe query string with url-encoded values.
        # just use it as is without filter in template.
        # it will get html encoded by the template renderer as it should be.
        # the output includes the '?' character. 
        from django.utils.http import urlquote
        get = self.filter.request.GET.copy()
        get[self.filter.varname] = self.valname
        ret = {}
        for varname in get:
            if varname is not None and len(varname.strip()) and len(get[varname].strip()) and (varname not in self.filter.query_vars_to_ignore):
                ret[varname] = urlquote(get[varname])
        return u'?' + u'&'.join([u'%s=%s' % (k, ret[k]) for k in ret])
    def href(self):
        # DEPRECATED - use query_string() instead
        # Returns a query string where the ampersand are already html encoded
        # Not good because we want url encoding not html encoding
        # Also there are other encoding cases to handle.
        # Finally the output must be filtered with |safe in a template
        # otherwise it will get encoded twice (&amp;amp;).
        ret = ''
        get = self.filter.request.GET.copy()
        get[self.filter.varname] = self.valname
        for varname in get:
            val = get[varname]
            if ret != '': ret += '&amp;'
            ret += '%s=%s' % (varname, val)
        return "?"+ret

# Subclasses to create and manage menu - each option is linked to an extension of the webpath 

class FilterWebPath(Filter):
    def get_input_parameter_internal(self):
        # extract from the web path the sequence after varname
        import re
        ret = ''
        m = re.search(r'%s(.*)' % self.varname, self.request.META['PATH_INFO'])
        if m is not None:
            ret = m.group(1).strip('/')
        return [ret]
    def add_option(self, option):
        return FilterOptionWebPath(option[0], option[1], self)
    def get_root(self):
        ret = ''
        import re
        m = re.search(r'(.*%s)' % self.varname, self.request.META['PATH_INFO'])
        if m is not None:
            ret = m.group(1).rstrip('/')
        return ret

class FilterOptionWebPath(FilterOption):
    """ One option in a filter e.g.: A to Z """
    def href(self):
        return self.filter.get_root()+'/'+self.valname
 
# Columns in a table (each filter represents a column with a toggable order)

class FilterColumn(Filter):
    def get_selected_column_name(self):
        return (self.get_selected_option()).valname
    def get_value(self):
        ''' careful: this function returns the suffix as well 
        so it does not necessarily match the value of the selected option'''
        ret = (self.get_selected_option()).valname
        if not self.is_ascending():
            ret += '-1'
        return ret
    def add_option(self, option):
        return FilterOptionColumn(option[0], option[1], self)
    def get_input_parameter_internal(self):
        ret = self.__get_column_value_and_order()
        return ret[0]
    def is_ascending(self):
        ret = self.__get_column_value_and_order()
        return ret[1]
    def __get_column_value_and_order(self):
        # if the value in GET = 'val-1' then return ('val', False)
        # if the value in GET = 'val' then return ('val', True)
        val = ''
        asc = True
        ret = get_request_var(self.request, self.varname, '', False)
        val = ret.rstrip('-1')
        if len(val) < len(ret):
            asc = False
        return [val, asc]

class FilterOptionColumn(FilterOption):
    def href(self):
        ret = ''
        get = self.filter.request.GET.copy()
        get[self.filter.varname] = self.valname
        if self.filter.is_ascending() and self.selected():
            get[self.filter.varname] = self.valname+'-1'
        for varname in get:
            val = get[varname]
            if ret != '': ret += '&amp;'
            ret += '%s=%s' % (varname, val)
        return "?"+ret
    
# Pagination

class FilterPagination(Filter):
    """ A filter, e.g. pagination """
    # all indices are 0-based # 
    def __init__(self, request, item_count=0, item_per_page=5, varname='pg'):
        super(FilterPagination, self).__init__('pagination', varname, request, 'page')
        self.item_per_page = int(item_per_page)
        self.item_count = int(item_count)
        import math
        self.last_page_index = 0
        if self.item_per_page > 0:
            self.last_page_index = int(math.floor((self.item_count - 1) / self.item_per_page))
        for i in range(0, self.last_page_index + 1):
            self.add_option([i+1, i])
    def get_last_index(self):
        return self.last_page_index
    def get_previous_index(self):
        ret = self.get_page_index() - 1
        if ret < 0: ret = 0
        return ret
    def get_next_index(self):
        ret = self.get_page_index() + 1
        if ret > self.last_page_index: ret = self.last_page_index
        return ret
    def get_page_index(self):
        # returns a 0 based index
        return int(self.get_value())
    def get_index_first_item_on_page(self):
        return self.get_page_index() * self.item_per_page
    def get_index_last_item_on_page(self):
        ret = self.item_count - 1
        if self.item_per_page > 0:
            ret_temp = ((self.get_page_index() + 1) * self.item_per_page) - 1
            if ret_temp < self.item_count: ret = ret_temp
        return ret
    def get_page_items(self, result_set):
        if result_set.count():
            result_set = result_set[self.get_index_first_item_on_page():self.get_index_last_item_on_page() + 1]
        return result_set
    def has_more_than_one_page(self):
        return self.last_page_index > 0

def get_request_var(request, varname, default='', multiple=False):
    if varname in request.GET:
        if multiple:
            return request.GET.getlist(varname)
        else:
            return ('%s' % request.GET[varname]).strip()
    return default

def get_az_filter_qs(request, query_set=None, field_names=None):
    # run a query to find all the used letters
    import re
    used_letters = {}
    if query_set is not None:
        from django.template.defaultfilters import slugify
        
        from cch.views.utils import get_concat_from_field_names
        query_set = query_set.extra(select={'azkey': get_concat_from_field_names(field_names)})
        values = query_set.values_list('azkey', flat=True)
        
        for value in values.iterator():
            if value:
                used_letters[slugify(value)[0].upper()] = 1
        
    ret = Filter('pages', 'pg', request, 'az')
    
    for letter in [chr(i) for i in range(ord('A'), ord('Z') + 1)]:
        FilterOption(letter, letter, ret, (u'%s' % letter) not in used_letters)
        
    return ret

def get_az_filter(request, model_name=None, field_names=None):
    from django.contrib.contenttypes.models import ContentType
    # editions_version => editions, version
    model_name = model_name.split('_')
    app_label, model_name = (model_name[0], '_'.join(model_name[1:]))
    # editions, version => Version class
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    # Version class => query set
    query_set = content_type.model_class().objects.all()
    return get_az_filter_qs(request, query_set, field_names)

