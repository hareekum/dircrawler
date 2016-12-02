# -*- coding: utf-8 -*-

"""
dircrawler.structures

This module contains all data structures used by dircrawler
"""


class FileStatus(object):
    """Class representing status of a file against snapshot"""
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"
    UNKNOWN = "UNKNOWN"
    UNCHANGED = "UNCHANGED"


class SnapshotState(object):
    """Class representing state of a file in a snapshot line"""
    def __init__(self, mod_ts=None):
        self.mod_ts = mod_ts
        self.visited = False
