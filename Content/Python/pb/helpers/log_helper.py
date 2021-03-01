import sys
import logging

from ..logger import Logger

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