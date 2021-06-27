from typing import OrderedDict
from collections import OrderedDict

import os
import csv
import ctypes

class SchemeField:
    std_to_c_types = {
        'str': str,
        'int8': lambda x: ctypes.c_int8(int(x)),
        'int16': lambda x: ctypes.c_int16(int(x)),
        'int32': lambda x: ctypes.c_int32(int(x)),
        'int64': lambda x: ctypes.c_int64(int(x)),
        'uint8': lambda x: ctypes.c_uint8(int(x)),
        'uint16': lambda x: ctypes.c_uint16(int(x)),
        'uint32': lambda x: ctypes.c_uint32(int(x)),
        'uint64': lambda x: ctypes.c_uint64(int(x)),
        'real32': lambda x: ctypes.c_float(float(x)),
        'real64': lambda x: ctypes.c_double(float(x)),
    }

    def __init__(self, field_name, std_type, flags):
        self.name = field_name
        self.std_type = std_type
        self.c_type = self.std_to_c_types[std_type]
        self.flags = flags

class SchemeTable:
    def __init__(self, table_name):
        self.name = table_name
        self.fields = []

    def add_field(self, new_field):
        self.fields.append(new_field)

    def get_field_names(self):
        return [field.name for field in self.fields]

    def get_field_c_types(self):
        return [field.c_type for field in self.fields]

    def get_record_len(self):
        return sum(8 if field.c_type is str else len(bytes(field.c_type(0))) for field in self.fields)

class SchemeManager:
    @classmethod
    def load(cls, csv_file_path):
        with open(csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            heads = next(csv_reader)
            rows = list(csv_reader)
            return cls(heads, rows)

    def __init__(self, heads, rows):
        schemes = OrderedDict()
        for row in rows:
            info = OrderedDict(zip(heads, row))            
            table_name = info['Table']
            if not table_name in schemes:
                schemes[table_name] = SchemeTable(table_name)
            
            scheme = schemes[table_name]
            scheme.add_field(SchemeField(info['Field'], info['Type'], info['Flags'].split('|')))

        self.schemes = schemes

    def get_schemes(self):
        return self.schemes

class Table:
    def __init__(self, heads, rows, parent=None):
        self.heads = heads
        self.rows = rows
        self.parent = parent

    def select(self, field_names):
        field_idxs = [self.heads.index(name) for name in field_names]
        return Table(field_names, [[row[idx] for idx in field_idxs] for row in self.rows], parent=self)

    def cast(self, field_types):
        def gen_casted_values(row):
            for idx, value in enumerate(row):
                yield field_types[idx](value)

        return Table(self.heads, [list(gen_casted_values(row)) for row in self.rows], parent=self)

    def dump(self, rec_len, blk_idx, encoding='utf-8'):
        def gen_bytes(rows):
            blk_idx_bytes = bytes(ctypes.c_int16(blk_idx))
            rec_cnt = len(rows)

            yield b'XDBC'
            yield bytes(ctypes.c_uint32(rec_cnt))            
            yield bytes(ctypes.c_uint16(rec_len))
            yield blk_idx_bytes            

            strs = []
            str_off = 0            
            for irow, vals in enumerate(rows):
                for icol, val in enumerate(vals):
                    if type(val) is str:
                        str_len = len(val)
                        yield bytes(ctypes.c_int16(str_len))
                        yield blk_idx_bytes                        
                        yield bytes(ctypes.c_int32(str_off))

                        strs.append(val)
                        strs.append('\0')
                        str_off += str_len + 1
                    else:
                        yield bytes(val)

            total_str = ''.join(strs)
            yield total_str.encode(encoding)
        
        return b''.join(gen_bytes(self.rows))
                

class CSVTable(Table):
    @classmethod
    def load(cls, csv_path):
        if os.path.isdir(csv_path):
            pass
        else:
            csv_file_path = csv_path + '.csv'
            with open(csv_file_path) as csv_file:
                csv_reader = csv.reader(csv_file)
                heads = next(csv_reader)
                rows = list(csv_reader)
                return cls(heads, rows)

    def find_unknown_field_names(self, field_names):
        return [name for name in field_names if not name in self.heads]

class DBCTool:
    def build(self, csv_root_path, dbc_root_path):        
        scheme_mgr = SchemeManager.load(os.path.join(csv_root_path, "_Schemes.csv"))
        schemes = scheme_mgr.get_schemes()
        for scheme in schemes.values():
            org_table = CSVTable.load(os.path.join(csv_root_path, scheme.name))

            field_names = scheme.get_field_names()
            assert(org_table.find_unknown_field_names(field_names) == [])
            selected_table = org_table.select(field_names)

            field_c_types = scheme.get_field_c_types()
            casted_table = selected_table.cast(field_c_types)

            rec_len = scheme.get_record_len()
            dbc_bytes = casted_table.dump(rec_len, blk_idx=0)
            with open(os.path.join(dbc_root_path, scheme.name + '.dbc'), 'wb') as dbc_file:
                dbc_file.write(dbc_bytes)