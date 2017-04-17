#!/usr/bin/env python
"""Trivial Person class.  Right now, just a name.  The idea is that you
can extend it with whatever records you want.  For a teeny personal project,
I can assume each person has a unique name.
"""

# pylint: disable=too-few-public-methods


class Person:
    """Trivial Person class.
    """

    def __init__(self, name):
        self.name = name
