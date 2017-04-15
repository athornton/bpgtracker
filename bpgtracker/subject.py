#!/usr/bin/env python
"""Simple Subject class: associates a person to a time series of data."""

from .person import Person
from .timeseries import Timeseries


class Subject:
    """Associates person with data time series.  If there are multiple
    entries for a particular date, the last one wins.
    """

    def __init__(self, person, timeseries):
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
