#!/usr/bin/env python
"""Read CSV file into list of BPGEntry objects.
"""

import csv
import datetime
import numpy as np
from .bpgentry import BPGEntry


class CSVHandler:
    """Read and write CSV files for BGPEntry objects.
    """

    def __init__(self, infile=None, outfile=None):
        """Create a CSVHandler object.
        """
        self.infilename = infile
        self.outfilename = outfile

    def load_entries_from_csv(self, filename=None):
        """Load entries from file; if filename is specified, resets
        handler object infilename.
        """
        if filename:
            self.infilename = filename
        if not self.infilename:
            raise ValueError("No CSV file to read")
        entries = []
        with open(self.infilename, "r", newline='') as infile:
            csvrdr = csv.reader(infile)
            next(csvrdr, None)  # Skip header line
            for row in csvrdr:
                date, systolic, diastolic, glucose = row
                entries.append(BPGEntry(date, systolic, diastolic, glucose))
        return entries

    def write_entries_to_csv(self, entries, filename=None):
        """Write timeseries entries to file; if filename is specified,
        resets handler object outfilename.
        """
        if filename:
            self.outfilename = filename
        if not self.outfilename:
            raise ValueError("No CSV file to write")
        with open(self.outfilename, "w", newline='') as outfile:
            csvwrt = csv.writer(outfile)
            csvwrt.writerow(BPGEntry.FIELDS)
            for entry in entries:
                datestr = datetime.datetime.strftime(entry.date, "%Y/%m/%d")
                row = [datestr]
                syst = entry.systolic
                dias = entry.diastolic
                gluc = entry.glucose
                if np.isnan(syst) and np.isnan(dias) and np.isnan(gluc):
                    continue  # Skip dates with no data.
                for val in [syst, dias, gluc]:
                    if np.isnan(val):
                        row.append('')
                    else:
                        row.append(str(val))
                csvwrt.writerow(row)
