# bpgtracker

Python classes for blood glucose and pressure tracking.  Testing push from 
Jupyterlab.

## Usage

Assuming your data is in `data.csv`:

### CLI

`bpgtracker -n "John Doe" -f data.csv`

### Python

```python
from bpgtracker import Subject

s=Subject("John Doe","data.csv")
s.plot_timeseries()
```

## CSV File format

bpgtracker expects to be able to read data from a CSV file.  This file
should have one header line and four fields per line:

`Date`, `Systolic`, `Diastolic`, `Blood Glucose`

Date should be in `YYYY/MM/DD` format.  The rest are integers (units
are mmHg for blood pressure and mg/dL for glucose).  If you specify
multiple readings for a given day, the last one wins.  If there is no
data for a particular measurement, leave the field empty.

