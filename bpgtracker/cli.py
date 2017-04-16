#!/usr/bin/env python
import argparse
from .csvhandler import CSVHandler
from .subject import Subject


def entrypoint():
    """Load and plot data for subject.
    """
    args = parse_args()
    if "name" not in args:
        raise ValueError("Name of subject must be specified")
    if "file" not in args:
        raise ValueError("CSV file containing time series must be specified")
    bpg = createbpgtracker(args.name, args.file)
    bpg.timeseries.create_plot()
    bpg.timeseries.display_plot()


def parse_args():
    """Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Read and plot blood pressure/glucose')
    parser.add_argument("-f", "--file", help="CSV file containing time series")
    parser.add_argument("-n", "--name", help="Name of subject")
    args = parser.parse_args()
    return args


def createbpgtracker(name, file):
    """Create new tracker from name and file.
    """
    handler = CSVHandler(file)
    entries = handler.load_from_csv(file)
    bpg = Subject(name, entries)
    return bpg

if __name__ == "__main__":
    entrypoint()
