import os
import sys
import contextlib

class OSHelper:
    __default_encoding = None

    @classmethod
    def get_default_encoding(cls):
        if cls.__default_encoding is None:
            cls.__default_encoding = cls.get_active_encoding()

        return cls.__default_encoding

    @classmethod
    def get_active_encoding(cls):
        if os.name == 'nt':
            from ctypes import cdll
            code_page = cdll.kernel32.GetACP()
            return f'cp{code_page}'
        else:
            return sys.getdefaultencoding()

    @classmethod
    def get_working_dir_path(cls):
        return os.getcwd()

    @contextlib.contextmanager
    @classmethod
    def push_working_dir_path(cls, new_dir):
        prv_dir = os.getcwd()
        os.chdir(new_dir)
        yield
        os.chdir(prv_dir)

