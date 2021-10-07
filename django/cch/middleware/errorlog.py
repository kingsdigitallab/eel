# $Id: errorlog.py 620 2010-08-05 10:55:36Z gnoel $

from datetime import datetime
from django.conf import settings
import sys
import traceback

# TODO: check this module: http://code.google.com/p/django-logging/wiki/Overview
# TODO: use python logging module to save to a file (http://www.djangosnippets.org/snippets/428/)
# TODO: more testing as this code *cannot* fail
# TODO: documentation

class ErrorLogMiddleware(object):
    """This middleware will log all the exceptions occurring on your site to a log file
        settings.py.ERROR_LOG_FILENAME is the path and name of the log file
        it will log the following information:
            Requested URL
            Request Dictionary (which includes POST, GET, request parameters...)
            Exception: the name and type of the exception
            Call Stack: a concise call stack (filename, function name, line number)
            
        Author: geoffroy.noel@kcl.ac.uk
    """    
    def process_exception(self, request, exception):
        """Automatically called by Django when an unhandled exception is raised"""
        # first check if the log file can be opened
        self.log("--------------------------------")
        self.log("URL: %s/%s (%s)" % (request.META['HTTP_HOST'], request.META['PATH_INFO'], request.META['REQUEST_METHOD']))
        self.log("Request: %s " % request)
        self.log("Exception: %s, %s" % (type(exception), exception))

        from django.views.debug import ExceptionReporter
        si = sys.exc_info()
        reporter = ExceptionReporter(request, *si)
        frames = reporter.get_traceback_frames()
        
        trace_str = "Call Stack:\n"
        for frame in frames:
            trace_str += "%s, %s" % (frame['filename'], frame['function'])
            if ('context_line' in frame):
                trace_str += ' line: %d' % frame['lineno']
            trace_str += "\n"
        self.log(trace_str)
        
    def log(self, message=''):
        try:
            f = open(settings.ERROR_LOG_FILENANE, 'a+')
            f.write("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] "+message+"\n")
            f.close()
        except:
            pass
        
            
        