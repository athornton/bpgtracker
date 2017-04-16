#!/usr/bin/env python
"""Timeseries class to represent sequence of measurements.
"""

import datetime
from collections import OrderedDict
import numpy as np
import matplotlib as ml
try:
    ipy = get_ipython()
except NameError:
    ml.use('TkAgg')
import matplotlib.pyplot as plt
from .bpgentry import BPGEntry


class Timeseries():
    """Timeseries class to represent sequence of BPGEntry measurements, at
    most one per date.  If multiples are specified in constructor for
    date, the last one wins.  They will be represented in
    lexically-sorted key order, which will also be date order.  Missing
    dates will be filled in with BPGEntries with null values.
    """

    _timeseries = OrderedDict()

    def __init__(self, timeseries=None):
        """Create a new timeseries object.
        """
        if timeseries:
            self.bulk_load(timeseries)

    def bulk_load(self, timeseries):
        """Import either a dict of BPGEntries or a list/tuple of them.
        If there are multiple entries for a date, the last one wins.
        """
        if timeseries is dict:
            tsd = timeseries
        elif isinstance(timeseries, (list, tuple)):
            tsd = {}
            for entry in timeseries:
                if not isinstance(entry, BPGEntry):
                    raise ValueError("Timeseries only accepts BGPEntries")
                key = datetime.datetime.strftime(entry.date, "%Y/%m/%d")
                tsd[key] = entry
        else:
            raise ValueError("Timeseries must be dict, list, or tuple")
        # now tsd has all the entries.  Now create an ordered dict sorted
        #  by key (which will sort lexically by date)
        self._timeseries = OrderedDict()
        sortedkeys = sorted(tsd.keys())
        lastkey = sortedkeys[-1]
        for key in sortedkeys:
            self._timeseries[key] = tsd[key]
            # Insert missing days
            moredays = True
            while key != lastkey and moredays:
                nextday = datetime.datetime.strftime(
                    datetime.datetime.strptime(key, "%Y/%m/%d") +
                    datetime.timedelta(days=1),
                    "%Y/%m/%d")
                if nextday in sortedkeys:
                    moredays = False
                key = nextday
                self._timeseries[key] = BPGEntry(key)

    def set(self, entry):
        """Add an item to the timeseries.
        """
        self.__setitem__(entry)

    def __setitem__(self, entry):
        """Add an item to the timeseries.
        """
        if not isinstance(entry, BPGEntry):
            raise ValueError("Timeseries only accepts BGPEntries")
        key = datetime.datetime.strftime(entry.date, "%Y/%m/%d")
        if key in self._timeseries:
            self._timeseries[key] = entry
            return
        # We need to resort.
        self._timeseries[key] = entry
        ordd = OrderedDict()
        for key in sorted(self._timeseries.keys()):
            ordd[key] = self._timeseries[key]
        self._timeseries = ordd

    def get(self, key):
        """Return a single timeseries entry.
        """
        return self.__getitem__(key)

    def __getitem__(self, key):
        """Return a single timeseries entry.
        """
        return self._timeseries[key]

    def keys(self):
        """Return a list of the timeseries keys.
        """
        return list(self._timeseries.keys())

    def values(self):
        """Return a list of the timeseries values.
        """
        return list(self._timeseries.values())

    def bulk_get(self):
        """Return the entire timeseries.
        """
        return self._timeseries

    def create_plot(self):
        """Create plot from timeseries.
        """
        slices = np.array([(x.date,
                            x.glucose,
                            x.systolic,
                            x.diastolic) for x in self.values()])
        dates = np.array(slices[:, 0])
        glucs = np.array(slices[:, 1])
        systs = np.array(slices[:, 2])
        diass = np.array(slices[:, 3])
        bpam = (systs + diass) / 2.0
        bpvr = (systs - diass) / 2.0

        plt.close('all')
        plt.figure(1)
        plt.errorbar(dates, bpam, bpvr, fmt='r')
        intdates = np.array([x.toordinal() for x in dates])
        fltbp = bpam.astype(np.float)
        idx = np.isfinite(fltbp)
        fpts = intdates[idx]
        fbp = fltbp[idx]
        bpt = np.polyfit(intdates[idx], fltbp[idx], 1)
        bpe = np.poly1d(bpt)
        plt.plot(intdates[idx], bpe(intdates[idx]), 'm--')
        plt.title("Blood Pressure")
        plt.ylabel("mmHg")
        plt.figure(2)
        plt.plot(dates, glucs, 'b')
        fltglc = glucs.astype(np.float)
        idx = np.isfinite(fltglc)
        bgt = np.polyfit(intdates[idx], fltglc[idx], 1)
        bge = np.poly1d(bgt)
        plt.plot(intdates[idx], bge(intdates[idx]), 'c--')
        plt.title("Blood Glucose")
        plt.ylabel("mg/dL")

    def display_plot(self):
        """Display the plotted data.
        """
        plt.show()
