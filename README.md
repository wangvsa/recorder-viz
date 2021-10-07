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
![example graphs](https://raw.githubusercontent.com/wangvsa/recorder-viz/main/tests/showoff.jpg)


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
    self.total_records: int
    self.num_files: int
    self.filemap: set()
    self.function_count: []


class RecorderMetadata(Structure):
    _fields_ = [
            ("total_ranks", c_int),
            ("start_ts", c_double),
            ("time_resolution", c_double),
            ("ts_buffer_elements", c_int),
            ("ts_compression_algo", c_int),
    ]

class Record(Structure):
    _fields_ = [
            ("tstart", c_double),
            ("tend", c_double),
            ("level", c_ubyte),
            ("func_id", c_ubyte),
            ("tid", c_int),
            ("arg_count", c_ubyte),
            ("args", POINTER(c_char_p)),
    ]
```


Here's an example on how to use the provided classes.

```python
from recorder_viz import RecorderReader

reader = RecorderReader("path/to/Recorder-traces-folder")

for rank in range(reader.GM.total_ranks):
    LM = reader.LMs[rank]
    print("Rank: %d, Number of trace records: %d" %(rank, LM.total_records))
```
