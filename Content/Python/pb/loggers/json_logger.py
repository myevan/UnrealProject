import logging
import json
import sys

from collections import OrderedDict

from ..log import Logger

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
