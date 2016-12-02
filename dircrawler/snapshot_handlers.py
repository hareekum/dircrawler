# -*- coding: utf-8 -*-

"""
dircrawler.snapshot_handlers

This module contains some snapshot handlers used for parsing snapshot files
"""

from . import structures

from . import utils


class AbstractSnapshotHandler(object):
    """Interface for snapshot handlers"""

    def parse(self, *args, **kwargs):
        raise NotImplementedError


class WhiteSpaceSeparatedSnapshotHandler(AbstractSnapshotHandler):
    """Class for parsing file states from a file having values split by whitespaces"""

    def parse(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                filepath, mtime = line.split()
                mod_ts = utils.timestamp_to_datetime(float(mtime))
                yield filepath, structures.SnapshotState(mod_ts=mod_ts)
