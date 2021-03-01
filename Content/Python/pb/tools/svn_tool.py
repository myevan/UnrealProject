import logging

from lxml import etree
from datetime import datetime

from ..cli import AppWrapper

class SVNHelper:
    @classmethod
    def parse_time(cls, text):
        return datetime.strptime(text, '%Y-%m-%dT%H:%M:%S.%fZ')

class SVNResult:
    def __init__(self, xml_text, encoding='utf-8'):
        self.encoding = encoding
        self.xml_tree = etree.fromstring(xml_text.encode(self.encoding))

    def __repr__(self):
        return etree.tostring(self.xml_tree, pretty_print=True).decode(self.encoding)

class SVNInfo(SVNResult):
    def __init__(self, *args, **kwargs):
        SVNResult.__init__(self, *args, **kwargs)
        self.ent_node = self.xml_tree.find('entry')
        self.key_values = {}

    def __cache_attr(self, key, node_name, attr_name, value_type=str):
        if not key in self.key_values:
            ent_node = self.ent_node.find(node_name) if node_name else self.ent_node
            attr_value = value_type(ent_node.get(attr_name))
            self.key_values[key] = attr_value
            return attr_value

        return self.key_values[key]

    def __cache_value(self, key, node_path=[], value_type=str):
        if not key in self.key_values:
            if node_path:
                cur_node = self.ent_node
                for node_name in node_path:
                    cur_node = cur_node.find(node_name)
            else:
                cur_node = self.ent_node.find(key)

            cur_value = value_type(cur_node.text)
            self.key_values[key] = cur_value
            return cur_value

        return self.key_values[key]        

    @property
    def kind(self): return self.__cache_value('kind', '', 'kind')

    @property
    def path(self): return self.__cache_attr('path', '', 'path')

    @property
    def revision(self): return self.__cache_attr('revision', '', 'revision', int)

    @property
    def url(self): return self.__cache_value('url')

    @property
    def rel_url(self): return self.__cache_value('realive-url')

    @property
    def root_url(self): return self.__cache_value('root-url', ['repository', 'root'])    

    @property
    def wc_abs_path(self): return self.__cache_value('abs-path', ['wc-info', 'wcroot-abspath'])

    @property
    def wc_depth(self): return self.__cache_value('depth', ['wc-info', 'depth'])

    @property
    def commit_author(self): return self.__cache_value('commit-author', ['commit', 'author'])

    @property
    def commit_time(self): return self.__cache_value('commit-time', ['commit', 'date'], value_type=SVNHelper.parse_time)

class SVNTool:
    def __init__(self, work_dir_path=".", exe_file_path='svn'):
        logging.info(f"svn_exe: {exe_file_path}")
        self.svn = AppWrapper(exe_file_path, "--xml")
        self.work_dir_path = work_dir_path

    def get_info(self, work_dir_path=""):
        return SVNInfo(self.svn.read_pipe('info', work_dir_path if work_dir_path else self.work_dir_path))
