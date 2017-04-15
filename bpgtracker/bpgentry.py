#!/usr/bin/env python
"""Class representing a blood pressure and glucose entry for a particular
date.
"""

import numpy as np
import datetime


class BPGEntry:
    """Class representing a blood pressure and glucose entry for a particular
    date.
    """

    FIELDS = ["Date", "Systolic", "Diastolic", "Glucose"]

    def __init__(self, date, systolic=None, diastolic=None, glucose=None):
        """Create the entry.
        """
        if not date:
            raise ValueError("Date is required for a BGPEntry.")
        self.date = self._normalize_datestr(date)
        # We take 0 to mean, "no reading", not "dead."  Same with None.
        if not systolic:
            systolic = np.nan
        else:
            systolic = int(systolic)
        if not diastolic:
            diastolic = np.nan
        else:
            diastolic = int(diastolic)
        if not glucose:
            glucose = np.nan
        else:
            glucose = int(glucose)
        self.systolic = systolic
        self.diastolic = diastolic
        self.glucose = glucose

    def __str__(self):
        """String representation.
        """
        datestr = datetime.datetime.strftime(self.date, "%Y/%m/%d")
        mstrs = [datestr]
        for val in self.systolic, self.diastolic, self.glucose:
            if val is np.nan:
                mstrs.append("-")
            else:
                mstrs.append(str(val))
        return "%s: %s/%s %s" % (mstrs[0], mstrs[1], mstrs[2], mstrs[3])

    def _normalize_datestr(self, datestr):
        """Parse our date string format.
        """
        return datetime.datetime.strptime(datestr, "%Y/%m/%d")
