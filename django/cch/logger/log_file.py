# $Id: log_file.py 659 2011-07-19 19:18:35Z gnoel $

from django.conf import settings


class LogFile:

    # PUBLIC METHODS

    def __init__(self, log_name='debug'):
        self.m_level = 2
        self.m_log_name = log_name
        self.showMicroseconds()

    def showMicroseconds(self, show_microseconds=False):
        self.m_show_microseconds = show_microseconds

    def setLevel(self, level):
        self.m_level = level

    def log(self, message, level=2):
        if level > self.m_level:
            return
        from datetime import datetime
        now = datetime.now()
        filename = '%s/logs/%s.log' % (settings.PROJECT_FILEPATH,
                                       self.m_log_name)
        time_pattern = "%y-%m-%d %H:%M:%S"
        if self.m_show_microseconds:
            time_pattern = time_pattern + '.%f'
        message = u'[%s] %s\n' % (now.strftime(time_pattern), message)
        f = open(filename, 'a')
        f.write(message.encode('utf-8'))
        f.close()

    def logTitle(self, message, level=2):
        self.log('\n------------------------------------\n        ' +
                 message + '\n------------------------------------', level)

    def logObject(self, object, level=2):
        message = u'%s' % object
        self.log(message, level)

    def logCallStack(self, message, level=2):
        self.log(message + ':\n' + self.getCallStack(), level)

    # INTERNAL METHODS

    def getCallStack(self):
        import traceback
        import re
        stack = traceback.extract_stack()
        ret = ''
        for call in stack:
            source_file_name = re.sub(r'^.*\\', '', call[0])
            if source_file_name == 'log_file.py':
                break
            #ret = ret + '\t%-30s%s:%s\n' % (call[2] + '()', call[1])
            ret = ret + '%s\n' % call[2]
            ret = ret + '\t%s\n' % (call[3])
            ret = ret + '\t%s:%s\n' % (call[0], call[1])
        return ret


log = LogFile()
logp = LogFile('perf')
logp.showMicroseconds(True)
