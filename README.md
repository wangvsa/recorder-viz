recorder-viz
=============

This is a python package which contains tools for processing [Recorder](https://github.com/uiuc-hpc/Recorder) traces.

Installation
-------------

`pip install recorder-viz`



Visualization
--------------

We relie on a few libraries for visualization. Please install them first.

Dependencies: [pandas](https://pandas.pydata.org/), [bokeh](https://docs.bokeh.org/) and [prettytable](https://pypi.org/project/PrettyTable/).

```python
import recorder_viz
from recorder_viz import RecorderReader

reader = RecorderReader("path/to/Recorder-traces-folder")
recorder_viz.generate_report(reader, "output.html")
```

The `generate_report` API will write out a HTML format visualization report.

The visualization process can be slow for large traces. We recommend to use it only for small scale runs, e.g., < 128 ranks runs.

Below are some example graphs generated from the [FLASH](http://flash.uchicago.edu) traces.
![showoff](./test/showoff.jpg)


Advanced Usages
-------------

The `RecorderReader` class contains all infomration about the Recorder traces.

```python
class RecorderReader:
    self.GM: instance of GlobalMetadata
    self.LMs: list of LocalMetadata objects, one for each rank
    self.records: self.records[i] is a list of Record objects of rank i.
```

`GlobalMetadta`, `LocalMetadata` and `Record` are three Python wrappers of C structures. 

```python
class LocalMetadata(Structure):
    _fields_ = [
            ("start_timestamp", c_double),
            ("end_timestamp", c_double),
            ("num_files", c_int),
            ("total_records", c_int),
            ("filemap", POINTER(c_char_p)),
            ("file_sizes", POINTER(c_size_t)),
            ("function_count", c_int*256),
    ]

class GlobalMetadata(Structure):
    _fields_ = [
            ("time_resolution", c_double),
            ("total_ranks", c_int),
            ("compression_mode", c_int),
            ("peephole_window_size", c_int),
    ]

class Record(Structure):
    _fields_ = [
            ("status", c_char),
            ("tstart", c_double),
            ("tend", c_double),
            ("func_id", c_ubyte),
            ("arg_count", c_int),
            ("args", POINTER(c_char_p)),
            ("res", c_int),
    ]
```


Here's an example on how to use the provided class.

```python
from recorder_viz import RecorderReader

reader = RecorderReader("path/to/Recorder-traces-folder")

for rank in range(reader.GM.total_ranks):
    LM = reader.LMs[rank]
    print("Rank: %d, Number of trace records: %d" %(rank, LM.total_records))
```
