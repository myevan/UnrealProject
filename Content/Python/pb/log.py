import logging
import sys

class Logger:
    def write(self, lv, msg, **kwargs):
        log_file = sys.stdout if lv < logging.ERROR else sys.stderr

        log_file.write(msg)
        log_file.write('\n')
        for key, value in kwargs.items():
            log_file.write('\t')
            log_file.write(key)
            log_file.write('\t')
            log_file.write(value)
            log_file.write('\n')

class LogHelper:
    __logger = Logger()

    @classmethod
    def bind(cls, logger):
        cls.__logger = logger

    @classmethod
    def info(cls, msg, **kwargs):
        cls.__logger.write(logging.INFO, msg, **kwargs)

    @classmethod
    def debug(cls, msg, **kwargs):
        cls.__logger.write(logging.DEBUG, msg, **kwargs)

    @classmethod
    def error(cls, msg, **kwargs):
        cls.__logger.write(logging.ERROR, msg, **kwargs)

    @classmethod
    def fatal(cls, msg, **kwargs):
        cls.__logger.write(logging.FATAL, msg, **kwargs)

    @classmethod
    def warning(cls, msg, **kwargs):
        cls.__logger.write(logging.WARNING, msg, **kwargs)