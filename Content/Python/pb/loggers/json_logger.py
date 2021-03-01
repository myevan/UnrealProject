import logging
import json
import sys

from ..logger import Logger
from collections import OrderedDict

class JsonLogger(Logger):
    def write(self, lv, msg, **kwargs):
        info = OrderedDict()
        info['__l'] = lv
        info['__m'] = msg
        info.update(kwargs)
        text = json.dumps(info)

        log_file = sys.stdout if lv < logging.ERROR else sys.stderr
        log_file.write(text)
        log_file.write('\n')
