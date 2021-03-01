from pb.tools.svn_tool import SVNTool
from .env import Environment

class SVNContext:
    __inst = None

    @classmethod
    def bind(cls, work_dir_path=""):
        cls.__inst = cls(work_dir_path)
        return cls.__inst

    @classmethod
    def get(cls):
        return cls.__inst

    def __init__(self, work_dir_path):
        env = Environment.get()
        self.svn_tool = SVNTool(
            work_dir_path=work_dir_path if work_dir_path else env.project_dir_path, 
            exe_file_path=env.join_engine_path('Engine', 'Binaries', 'ThirdParty', 'svn', 'Win64', 'svn.exe'))        

        self.svn_info = None

    def get_info(self):
        if not self.svn_info:        
            self.svn_info = self.svn_tool.get_info()
        return self.svn_info
