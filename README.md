recorder-viz
=============

This is a python package which contains tools for processing [Recorder](https://github.com/uiuc-hpc/Recorder) traces.

Usnage
--------

Install it using pip: `pip install recorder-viz`


Below is a simple code snippet shows how to use the provided class `RecorderReader`. 

Copy it to test.py and `run python test.py [path/to/Recorder traces folder]`

```python

#!/usr/bin/env python
# encoding: utf-8

import sys
from recorder_viz import RecorderReader

reader = RecorderReader(sys.argv[1])

for rank in range(reader.GM.total_ranks):
    LM = reader.LMs[rank]
    print("Rank: %d, Number of trace records: %d" %(rank, LM.total_records))
```
