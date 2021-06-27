import unreal
import os

from pb.patterns.singleton import singleton

@singleton
class Environment:
    def __init__(self):
        self.__prj_file_path = ""
        self.__prj_dir_path = ""
        self.__eng_dir_path = ""
        self.__svn_exe_path = "svn"

    @property
    def project_file_path(self):
        if not self.__prj_file_path:
            self.__prj_file_path = os.path.realpath(unreal.Paths.get_project_file_path())

        return self.__prj_file_path
    
    @property
    def project_dir_path(self):
        if not self.__prj_dir_path:
            self.__prj_dir_path = os.path.dirname(self.project_file_path)

        return self.__prj_dir_path

    @property
    def engine_dir_path(self):
        if not self.__eng_dir_path:
            self.__eng_dir_path = os.path.realpath(unreal.Paths.root_dir())

        return self.__eng_dir_path

    def join_engine_path(self, *args):
        return os.path.join(self.engine_dir_path, *args)

