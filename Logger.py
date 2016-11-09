'''Logger logging via syslog

usage::

    from Logger import Logger

    Logger.info('this is a test message')
'''

__all__ = ['Logger']

import syslog

class Logger(object):
    syslog.openlog(logoption = syslog.LOG_PID, facility = syslog.LOG_LOCAL0)

    @staticmethod
    def _log(pri, msg):
        syslog.syslog(pri, msg)

    @staticmethod
    def debug(msg):
        Logger._log(syslog.LOG_DEBUG, msg)

    @staticmethod
    def info(msg):
        Logger._log(syslog.LOG_INFO, msg)

    @staticmethod
    def warn(msg):
        Logger._log(syslog.LOG_WARNING, msg)

    @staticmethod
    def error(msg):
        Logger._log(syslog.LOG_ERR, msg)

    @staticmethod
    def fatal(msg):
        Logger._log(syslog.LOG_CRIT, msg)


