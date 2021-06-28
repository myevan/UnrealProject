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

    def dump8(self, rec_len, blk_idx, sep=b'\0'):
        def gen_bytes(rows):
            blk_idx_bytes = bytes(ctypes.c_int16(blk_idx))
            rec_cnt = len(rows)

            yield b'DBC8'
            yield bytes(ctypes.c_uint32(rec_cnt))            
            yield bytes(ctypes.c_uint16(rec_len))
            yield blk_idx_bytes            

            utf8_strs = []
            utf8_off = 0

            for irow, vals in enumerate(rows):
                for icol, val in enumerate(vals):
                    if type(val) is str:
                        utf8_str = val.encode('utf-8')
                        utf8_len = len(utf8_str)
                        yield bytes(ctypes.c_int16(utf8_len))
                        yield blk_idx_bytes                        
                        yield bytes(ctypes.c_int32(utf8_off))

                        utf8_strs.append(utf8_str + sep)
                        utf8_off += utf8_len + len(sep)
                    else:
                        yield bytes(val)

            yield b''.join(utf8_strs)
        
        return b''.join(gen_bytes(self.rows))

    def dumpu(self, rec_len, blk_idx, sep=b'\t'):
        def gen_bytes(rows):
            blk_idx_bytes = bytes(ctypes.c_int16(blk_idx))
            rec_cnt = len(rows)

            yield b'DBCU'
            yield bytes(ctypes.c_uint32(rec_cnt))            
            yield bytes(ctypes.c_uint16(rec_len))
            yield blk_idx_bytes            

            utf8_strs = []
            uni_off = 0
            uni_sep = sep.decode('utf-8')

            for irow, vals in enumerate(rows):
                for icol, val in enumerate(vals):
                    if type(val) is str:
                        uni_len = len(val)

                        yield bytes(ctypes.c_int16(uni_len))
                        yield blk_idx_bytes                        
                        yield bytes(ctypes.c_int32(uni_off))

                        utf8_strs.append(val.encode('utf8') + sep)
                        uni_off += len(val) + len(uni_sep)
                    else:
                        yield bytes(val)

            yield b''.join(utf8_strs)

        return b''.join(gen_bytes(self.rows))

    def dumpi(self, rec_len, blk_idx, sep=b'\t'):
        def gen_bytes(rows, uni_strs):
            blk_idx_bytes = bytes(ctypes.c_int16(blk_idx))
            rec_cnt = len(rows)

            yield b'DBCI'
            yield bytes(ctypes.c_uint32(rec_cnt))            
            yield bytes(ctypes.c_uint16(rec_len))

            uni_sep = sep.decode('utf-8')

            for irow, vals in enumerate(rows):
                for icol, val in enumerate(vals):
                    if type(val) is str:
                        uni_str = val
                        uni_str_len = len(uni_str)
                        uni_str_idx = len(uni_strs)

                        yield bytes(ctypes.c_int16(uni_str_len))
                        yield blk_idx_bytes                        
                        yield bytes(ctypes.c_int32(uni_str_idx))

                        uni_strs.append(uni_str + uni_sep)
                    else:
                        yield bytes(val)

        uni_strs = [] 
        main_bytes = b''.join(gen_bytes(self.rows, uni_strs))
        utf8_bytes = b''.join(uni_str.encode('utf8') for uni_str in uni_strs)
        return (main_bytes, utf8_bytes)


class CSVTable(Table):
    @classmethod
    def load(cls, csv_path):
        if os.path.isdir(csv_path):
            print(f"CSV_DIR: {csv_path}")
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
            dbc8_bytes = casted_table.dump8(rec_len, blk_idx=0)
            with open(os.path.join(dbc_root_path, scheme.name + '.dbc8'), 'wb') as dbc8_file:
                dbc8_file.write(dbc8_bytes)

            dbcu_bytes = casted_table.dumpu(rec_len, blk_idx=0)
            with open(os.path.join(dbc_root_path, scheme.name + '.dbcu'), 'wb') as dbcu_file:
                dbcu_file.write(dbcu_bytes)

            dbci_bytes, tsv_bytes = casted_table.dumpi(rec_len, blk_idx=0)
            with open(os.path.join(dbc_root_path, scheme.name + '.dbci'), 'wb') as dbci_file:
                dbci_file.write(dbci_bytes)
            with open(os.path.join(dbc_root_path, scheme.name + '.tsv'), 'wb') as tsv_file:
                tsv_file.write(tsv_bytes)

if __name__ == '__main__':
    DBCTool().build('.', '.')
