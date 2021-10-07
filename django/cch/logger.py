# $Id: logger.py 620 2010-08-05 10:55:36Z gnoel $

'''
    Log messages to a log file.
    The path of the log file is settings.PROJECT_FILEPATH+'/logs/debug.log'.
    Make sure you this directory exists and is writable.
'''
import settings 

class Logger:
    
    def __init__(self):
        self.level = 2
    
    def setLevel(self, level):
        self.level = level
    
    def log(self, message, level=2):
        if level > self.level: return
        from datetime import datetime
        now = datetime.now()
        filename = settings.PROJECT_FILEPATH+'/logs/debug.log'
        message = u'[%s] %s\n' % (now.strftime("%y-%m-%d %H:%M:%S"), message)
        f = open(filename, 'a')
        f.write(message.encode('utf-8'))
        f.close()
    
    def logTitle(self, message, level=2):
        self.log('\n------------------------------------\n        '+message+'\n------------------------------------', level)

log = Logger()
