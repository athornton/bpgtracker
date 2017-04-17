#!/usr/bin/env python
"""Simple Subject class: associates a person to a time series of data."""

from .csvhandler import CSVHandler
from .person import Person
from .timeseries import Timeseries


class Subject:
    """Associates person with data time series.  If there are multiple
    entries for a particular date, the last one wins.
    """

    def __init__(self, person, timeseries=None):
        """Create Subject association of person to timeseries.
        """
        if person is None:
            raise ValueError("Subject must be associated with a person.")
        if person is Person:
            self.person = person
        else:
            self.person = Person(person)
        self.timeseries = None
        if timeseries is not None:
            self.timeseries = Timeseries(timeseries)

    def import_timeseries(self, filename):
        """Import timeseries from CSV file
        """
        self.timeseries = Timeseries(filename)

    def export_timeseries(self, filename):
        """Export timeseries to CSV file
        """
        if self.timeseries is None:
            raise ValueError("Cannot export empty timeseries")
        csvh = CSVHandler(outfile=filename)
        entries = self.timeseries.values()
        csvh.write_entries_to_csv(entries)

    def plot_timeseries(self):
        """Create and display plot from timeseries data"""
        if self.timeseries is not None:
            self.timeseries.create_plot(name=self.person.name)
            self.timeseries.display_plot()
