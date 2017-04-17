#!/usr/bin/env python
"""Timeseries class to represent sequence of measurements.
"""

import datetime
from collections import OrderedDict
import numpy as np
import matplotlib as ml
# pylint: disable=invalid-name, wrong-import-position
try:
    ipy = get_ipython()
except NameError:
    # OS X accomodation
    ml.use('TkAgg')
import matplotlib.pyplot as plt
from .bpgentry import BPGEntry
from .csvhandler import CSVHandler


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
        """Import either a dict of BPGEntries or a list/tuple of them.  If
        the timeseries argument is a string, try to load the file with the
        corresponding name.

        If there are multiple entries for a date, the last one wins.
        """
        if isinstance(timeseries, dict):
            tsd = timeseries
        elif isinstance(timeseries, (str, list, tuple)):
            if isinstance(timeseries, str):
                # Load timeseries from file.
                csvh = CSVHandler(timeseries)
                timeseries = csvh.load_entries_from_csv()
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

    # pylint: disable=too-many-locals, too-many-statements
    def create_plot(self, name=None):
        """Create plot from timeseries, optionally with subject name attached.
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
        intdates = np.array([x.toordinal() for x in dates])
        fltsys = systs.astype(np.float)
        fltdia = diass.astype(np.float)
        # Numpy doesn't play well with pylint.
        # pylint: disable=no-member
        idx = np.isfinite(fltsys)  # Assume systolic/diastolic are same
        fpts = intdates[idx]
        # 1.96 std. dev. is 95% confidence.
        bins = np.array([1.96, 1.0, -1.0, -1.96])
        fbs = fltsys[idx]
        fbd = fltdia[idx]
        bps = np.polyfit(fpts, fbs, 1)
        bpse = np.poly1d(bps)
        bpd = np.polyfit(fpts, fbd, 1)
        bpde = np.poly1d(bpd)
        smodel = bpse(fpts)
        dmodel = bpde(fpts)
        # Add one standard deviation and 95% confidence intervals
        #  for each of systolic and diastolic
        self._plot_errors(fpts, smodel, fbs.std(), bins, ['thistle', 'plum'])
        self._plot_errors(fpts, dmodel, fbd.std(), bins, ['bisque', 'wheat'])
        # Add high-blood-pressure threshold
        plt.plot(fpts, np.array([140.0 for x in fpts]), color='0.5',
                 linestyle='dashed')
        plt.plot(fpts, np.array([90.0 for x in fpts]), color='0.5',
                 linestyle='dashed')
        # Plot data and then regression last so they go on top
        plt.errorbar(dates, bpam, bpvr, fmt='r,')
        plt.plot(fpts, smodel, 'm--')
        plt.plot(fpts, dmodel, color='tan', linestyle='dashed')
        plotname = "Blood Pressure"
        if name:
            plotname += " for %s" % name
        plt.title(plotname)
        plt.gcf().canvas.set_window_title(plotname)
        plt.ylabel("mmHg")
        plt.figure(2)
        plt.plot(dates, glucs, 'b')
        fltglc = glucs.astype(np.float)
        idx = np.isfinite(fltglc)
        fpts = intdates[idx]
        fglc = fltglc[idx]
        bgt = np.polyfit(fpts, fglc, 1)
        bge = np.poly1d(bgt)
        gmodel = bge(fpts)
        # Add one standard deviation and 95% confidence intervals
        self._plot_errors(fpts, gmodel, fglc.std(), bins,
                          ['skyblue', 'deepskyblue'])
        # Plot data and then regression last so they go on top
        plt.plot(dates, glucs, 'b')
        plt.plot(fpts, gmodel, 'c--')
        plotname = "Blood Glucose"
        if name:
            plotname += " for %s" % name
        plt.title(plotname)
        plt.gcf().canvas.set_window_title(plotname)
        plt.ylabel("mg/dL")
        plt.ylim(60, 150)

    # pylint: disable=no-self-use, too-many-arguments
    def _plot_errors(self, xrg, model, stddev, bands, colors):
        if len(bands) != 2 * len(colors):
            raise ValueError("Number of bands must be 2x number of colors")
        bandvals = [x * stddev for x in bands]
        colorbands = [x for x in colors]
        colorbands.extend([x for x in colors[::-1]])
        idx = 0
        for band in bandvals:
            plt.plot(xrg, model + band,
                     color=colorbands[idx], linestyle='dashed')
            idx += 1

    # pylint: disable=no-self-use
    def display_plot(self):
        """Display the plotted data.
        """
        plt.show()
