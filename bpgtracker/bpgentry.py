#!/usr/bin/env python
"""Class representing a blood pressure and glucose entry for a particular
date.
"""

import datetime
import numpy as np


# pylint: disable=too-few-public-methods
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
        if isinstance(date, str):
            self.date = datetime.datetime.strptime(date, "%Y/%m/%d")
        elif isinstance(date, datetime.datetime):
            self.date = date
        else:
            errstr = "Date must be a YYYY/MM/DD string or a datetime object."
            raise ValueError(errstr)
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
