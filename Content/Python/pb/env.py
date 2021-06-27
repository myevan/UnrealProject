from pb.patterns.singleton import singleton

import os

@singleton
class Environment:
    def __init__(self):
        this_file_path = os.path.realpath(__file__)
        this_dir_path = os.path.dirname(this_file_path)
        self.__prj_dir_path = os.path.realpath(os.path.join(this_dir_path, "..", "..", ".."))
        self.__content_dir_path = ""
        self.__csv_root_path = ""
        self.__dbc_root_path = ""

    @property
    def project_dir_path(self):
        return self.__prj_dir_path

    @property
    def content_dir_path(self):
        if not self.__content_dir_path:
            self.__content_dir_path = os.path.join(self.project_dir_path, "Content")
        
        return self.__content_dir_path

    @property
    def csv_root_path(self):
        if not self.__csv_root_path:
            self.__csv_root_path = os.path.join(self.content_dir_path, "CSVs")
        
        return self.__csv_root_path

    @property
    def dbc_root_path(self):
        if not self.__dbc_root_path:
            self.__dbc_root_path = os.path.join(self.content_dir_path, "DBCs")
        
        return self.__dbc_root_path

