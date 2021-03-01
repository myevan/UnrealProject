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
