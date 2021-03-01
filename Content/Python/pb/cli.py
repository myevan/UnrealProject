# -*- coding:utf8 -*-
import os
import sys
import subprocess
import contextlib

from pb.log import LogHelper

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


class AppWrapper:
    class Error(Exception):
        def __init__(self, name, args, exit_code, error_text=""):
            Exception.__init__(self, name)
            self.name = name
            self.args = args
            self.exit_code = exit_code
            self.error_text = error_text

        def __str__(self):            
            if self.error_text:
                if '\n' in self.error_text:
                    tail = f"\n{self.error_text}"
                else:
                    tail = f":{self.error_text}"
            else:
                tail = ""

            return f"{self.__class__.__name__}<{self.name}>(args={self.args}, exit_code={self.exit_code}){tail}"    

    def __init__(self, *main_args, strict=True, encoding=OSHelper.get_default_encoding()):        
        self.main_args = list(main_args)
        self.strict = strict
        self.encoding = encoding

    def run(self, *sub_args):
        total_args = self.main_args + list(sub_args)
        LogHelper.debug("cli", func="run", line=' '.join(total_args))

        exit_code = subprocess.call(total_args)
        if self.strict and exit_code != 0:
            raise self.Error('RUN', total_args, exit_code)

    def gen_pipe_lines(self, *sub_args):
        total_args = self.main_args + list(sub_args)
        LogHelper.debug("cli", func="gen_pipe_lines", line=' '.join(total_args))

        proc = subprocess.Popen(
            total_args,
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        while proc.returncode is None:
            for line in proc.stdout:
                yield line.decode(self.encoding) if self.encoding else line
            else:
                proc.poll()

    def read_pipe(self, *sub_args):
        total_args = self.main_args + list(sub_args)
        LogHelper.debug("cli", func="read_pipe", line=' '.join(total_args))

        proc = subprocess.Popen(
            total_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        output, error = proc.communicate()
        if self.strict and proc.returncode != 0:
            raise self.Error('READ_PIPE', total_args, proc.returncode)

        return output.decode(self.encoding) if self.encoding else output

    def write_pipe(self, data):
        total_args = self.main_args + list(sub_args)
        LogHelper.debug("cli", func="write_pipe", line=' '.join(total_args))

        proc = subprocess.Popen(
            self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        proc.stdin.write(data)
        proc.stdin.close()
        if proc.wait():
            error_text = proc.stderr.read()
            raise self.Error('WRITE_PIPE', total_args, proc.returncode, error_text)

        return proc.stdout.read()
