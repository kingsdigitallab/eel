'''
Created on 28 Aug 2010

@author: Geoffroy

TODO:
These classes need to be optimised and made more abstract.
1. Work directly at the string level rather than unpacking and packing 
the serialised version each time we need to access or modify the array.
2. Don't assume anything about the query string.
3. consider refactoring this class so it only works with strings (no array) 
and it doesn't know about the database or the webpaths. (only use th current URL as an input)  
'''

from ootw.plays.models import Work, Author

class StringArray(object):
    ''' Need to be optimised.
        Here we are unpacking and repacking the array for each http request
        it would be more efficient to directly work on the string encoded array.
    '''
    
    def __init__(self, max_size = 2024):
        self.max_size = max_size
        self.items = []
    
    def addItem(self, item):
        item_str = item.getString()
        # too long for our buffer, we can't add it
        if len(self.items):
            item_str = '|' + item_str
        if len(item_str) > self.max_size: return
        # remove previous item if it is similar to the new one
        while True:
            if len(self.items) == 0: break
            if not self.items[-1].similarTo(item): break
            self.items.pop()
        # make space for the new item
        array_len = self.getLen()
        while array_len + len(item_str) > self.max_size:
            # remove the first item
            if len(self.items) > 1: array_len = array_len -1
            itemf = self.items.pop(0)
            array_len = array_len - len(itemf.getString())
        # now add the new item
        self.items.append(item)
    
    def getLen(self):
        ret = 0
        for item in self.items:
            if ret > 0: ret = ret + 1
            ret = ret + len(item.getString())
        return ret
    
    def setFromString(self, array_str):
        self.items = []
        for item_str in array_str.split('|'):
            item = self.__getItemFromString(item_str)
            if item is not None: 
                self.items.append(item)
    
    def __getItemFromString(self, item_str):
        # read the first letter as it indicates the type of item
        ret = None
        if item_str[0] in ['a', 'p']:
            ret = ActivityItemRecord('')
        if item_str[0] == 's':
            ret = ActivityItemSearch('')
        if ret is not None:
            ret.setFromString(item_str)
        return ret
    
    def getItems(self):
        return self.items
        
    def getItemsReversed(self):
        ret = self.getItems()[:]
        ret.reverse()
        return ret
    
    def getRecentItemsReversed(self):
        ret = self.getItemsReversed()[0:15]
        return ret
    
    def getAsString(self):
        ret = ''
        for item in self.items:
            if len(ret) > 0: ret = ret + '|'
            ret = ret + item.getString()
        return ret

class ActivityCookie(StringArray):
    def __init__(self, request, cookie_name = 'VIEWS', max_size=2000):
        super(ActivityCookie, self).__init__(max_size)
        self.cookie_name = cookie_name
        self.request = request
        if cookie_name in request.COOKIES:
            self.setFromString(request.COOKIES[cookie_name])
    def addItemToResponse(self, response, activity_item):
        self.addItem(activity_item)
        response.set_cookie(self.cookie_name, self.getAsString())
    
class ActivityItem(object):
    ''' Used to store two types of items:
        * action on the search page, for the moment limited to the search phrase. (s)
        * action on the author or play page. (a,p)'''
    def setFromString(self, item_str):
        # to be overridden
        pass
    def getString(self):
        ''' format: [ACTION_CODE][OPTIONS]
            for s: OPTIONS is any of the query string parameters but without the s_ prefix
            for a/p: OPTION is just the record id
        '''
        ret = ''
        return ret
    def similarTo(self, other_item):
        return self.getString() == other_item.getString()
    def getRecordType(self):
        return self.record_type
    def getRecord(self):
        return None

'''
    Specific types of items.
    The following items know about the ootw database and web urls.
'''

class ActivityItemRecord(ActivityItem):
    def __init__(self, record_type='a', recordid=0):
        self.recordid = recordid
        self.record_type = record_type
    def setFromString(self, item_str):
        self.record_type = item_str[0]
        self.recordid = item_str[1:]
    def getString(self):
        return '%s%s' % (self.record_type, self.recordid)
    def getRecord(self):
        ret = None
        if self.record_type == 'a':
            from ootw.plays.models import Author
            records = Author.objects.filter(id=self.recordid)
        if self.record_type == 'p':
            from ootw.plays.models import Work
            records = Work.objects.filter(id=self.recordid)
        if records.count() == 1: ret = records[0]
        return ret
        
#    def similarTo(self, other_item):
#        return other_item.__class__.__name__ == self.__class__.__name__ and other_item.recordid == self.recordid
        
class ActivityItemSearch(ActivityItem):
    def __init__(self, search_phrase):
        # get all the parameters from the query string or from the search filters
        self.search_phrase = search_phrase
        self.record_type = 's'
    def setFromString(self, item_str):
        self.search_phrase = item_str[1:]
    def getString(self):
        return self.record_type + self.search_phrase
    def getSearchPhrase(self):
        return self.search_phrase
#    def similarTo(self, other_item):
#        # TODO: also check the search phrase but disregard the filters
#        return other_item.__class__.__name__ == self.__class__.__name__ and other_item.search_phrase == self.search_phrase
