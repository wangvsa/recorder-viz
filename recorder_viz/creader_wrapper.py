#!/usr/bin/env python
# encoding: utf-8
from ctypes import *
import os, glob

class RecorderMetadata(Structure):
    _fields_ = [
            ("total_ranks", c_int),
            ("start_ts", c_double),
            ("time_resolution", c_double),
            ("ts_buffer_elements", c_int),
            ("ts_compression_algo", c_int),
    ]

class LocalMetadata():
    def __init__(self, func_list, records, total_records):
        self.total_records = total_records
        self.num_files =0
        self.filemap = set()
        self.function_count = [0] * 256

        for idx in range(total_records):
            r = records[idx]

            # Ignore user functions for now
            if r.func_id < len(func_list):
                func = func_list[r.func_id]
                self.function_count[r.func_id] += 1

            if "MPI" in func or "H5" in func: continue

            if "dir" in func: continue
            if "open" in func or "close" in func or "creat" in func \
                or "seek" in func or "sync" in func:
                fstr = r.args[0]
                self.filemap.add(fstr if type(fstr)==str else fstr.decode('utf-8'))

        self.num_files = len(self.filemap)


class PyRecord(Structure):
    # The fields must be identical as PyRecord in reader.h
    _fields_ = [
            ("tstart",    c_double),
            ("tend",      c_double),
            ("level",     c_ubyte),
            ("func_id",   c_ubyte),
            ("tid",       c_int),
            ("arg_count", c_ubyte),
            ("args",      POINTER(c_char_p)),    # Note in python3, args[i] is 'bytes' type
    ]

    # In Python3, self.args[i] is 'bytes' type
    # For compatable reason, we convert it to str type
    # and will only use self.arg_strs[i] to access the filename
    def args_to_strs(self):
        arg_strs = [''] * self.arg_count
        for i in range(self.arg_count):
            if(type(self.args[i]) == str):
                arg_strs[i] = self.args[i]
            else:
                arg_strs[i] = self.args[i].decode('utf-8')
        return arg_strs

'''
GM: Global Metadata
LMs: List of Local Metadata
records: List (# ranks) of Record*, each entry (Record*) is a list of records for that rank
'''
class RecorderReader:
    def str2char_p(self, s):
        return c_char_p( s.encode('utf-8') )

    def __init__(self, logs_dir):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        search_path = os.path.abspath(os.path.join(current_dir, 'libreader*.so'))

        libreader_path = ''
        found = glob.glob(search_path)
        if len(found) == 1:
            libreader_path = found[0]

        libreader = cdll.LoadLibrary(libreader_path)
        libreader.read_all_records.restype = POINTER(POINTER(PyRecord))

        self.GM = RecorderMetadata()
        libreader.read_metadata(self.str2char_p(logs_dir + "/recorder.mt"), pointer(self.GM))


        SizeArray = c_size_t * self.GM.total_ranks
        counts = SizeArray()
        self.records = libreader.read_all_records(self.str2char_p(logs_dir), counts)

        self.load_func_list(logs_dir + "/recorder.mt")

        self.LMs = []
        for rank in range(self.GM.total_ranks):
            LM = LocalMetadata(self.funcs, self.records[rank], counts[rank])
            self.LMs.append(LM)
            print("Rank: %d, intercepted calls: %d, accessed files: %d" %(rank, counts[rank], LM.num_files))

    def load_func_list(self, global_metadata_path):
        with open(global_metadata_path, 'rb') as f:
            f.seek(32, 0)
            self.funcs = f.read().splitlines()
            self.funcs = [func.decode('utf-8') for func in self.funcs]


'''
if __name__ == "__main__":
    import sys
    reader = RecorderReader(sys.argv[1])
'''
