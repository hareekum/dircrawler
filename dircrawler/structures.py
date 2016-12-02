# -*- coding: utf-8 -*-

"""
dircrawler.structures

This module contains all data structures used by dircrawler
"""


class FileStatus(object):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"
    UNKNOWN = "UNKNOWN"


class FileState(object):
    def __init__(self, mod_ts=None):
        self.mod_ts = mod_ts
        self.visited = False
