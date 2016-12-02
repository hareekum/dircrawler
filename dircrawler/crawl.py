#!/usr/bin/env python

"""
dircrawler.crawl

This module contains the crux of dircrawler functionality. This module is also designed to be
run from the command line
"""

import os
from pydoc import locate
import sys
import argparse

import progressbar

from . import utils
from .structures import FileStatus


class DirCrawler(object):
    def __init__(self, dirpath, progress=False, snapshot_file=None, snapshot_handler=None):
        self.dirpath = dirpath
        self.progress = progress
        self.snapshot = {}
        if snapshot_file and snapshot_handler:
            self._parse_snapshot(snapshot_file, snapshot_handler)
        self.file_count = self._get_file_count() if self.progress else None

    def _parse_snapshot(self, filepath, klass):
        """Updates snapshot with filepath and state obtained from snapshot handler class"""
        snapshot_class = locate(klass)
        for filepath, state in snapshot_class().parse(filepath):
            self.snapshot.update({filepath: state})

    def _walk_dir(self):
        """Generator that walks through given dirpath and yields file paths"""
        for root, dirs, files in os.walk(self.dirpath):
            for filename in files:
                yield os.path.abspath(os.path.join(root, filename))

    def _get_file_count(self):
        """Returns total number of files in a directory tree"""
        file_count = 0
        for _ in self._walk_dir():
            file_count += 1
        return file_count

    def _get_file_state(self, filepath):
        """Returns state of a given filepath diffing against snapshot"""
        if filepath not in self.snapshot:
            return FileStatus.ADDED

        current_mod_ts = utils.mod_ts_in_utc(filepath)
        snapshot_mod_ts = self.snapshot[filepath].mod_ts
        self.snapshot[filepath].visited = True
        if current_mod_ts > snapshot_mod_ts:
            return FileStatus.MODIFIED
        elif current_mod_ts == snapshot_mod_ts:
            return FileStatus.UNCHANGED
        else:
            # This should not happen
            return FileStatus.UNKNOWN

    def traverse(self, transformer=None):
        """
        Recursively traverses through a directory, computes state of a file,
        applies transformation if specified and returns a tuple of
        (file path, state, transformed output)
        """
        if self.progress:
            bar = progressbar.ProgressBar(
                widgets=['Progress: ', progressbar.Percentage(), ' | ', progressbar.ETA()],
                max_value=self.file_count, redirect_stdout=True)
        count = 0
        transformer_method = locate(transformer)().transform if transformer else lambda x: ''

        # Walk through all files in dirpath
        for filepath in self._walk_dir():
            yield filepath, self._get_file_state(filepath), transformer_method(filepath)
            if self.progress:
                bar.update(count)
            count += 1

        # Check for files in snapshot but not in dirpath
        for filepath, state in self.snapshot.iteritems():
            if not state.visited:
                yield filepath, FileStatus.REMOVED, ''
        if self.progress:
            bar.finish()


def handle_args():
    """Handle command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True, help='Directory path to traverse')
    parser.add_argument('-sf', '--snapshot-file', required=False, help='Snapshot file path')
    parser.add_argument('-sh', '--snapshot-handler', required=False,
                        help='Import path of snapshot handler class')
    parser.add_argument('-t', '--transformer', required=False,
                        help='Import path of transformer class')

    parser.add_argument('-p', '--progress', required=False, action='store_true', default=False,
                        help='Show progress bar')

    options = parser.parse_args()
    if options.snapshot_file and options.snapshot_handler is None:
        parser.error('--snapshot-file requires --snapshot-handler.')
    return options


def main():
    options = handle_args()
    dircrawler = DirCrawler(options.directory, progress=options.progress,
                            snapshot_file=options.snapshot_file,
                            snapshot_handler=options.snapshot_handler)
    for filepath, status, transformed in dircrawler.traverse(transformer=options.transformer):
        print "%s\t%s\t%s" % (status, transformed, filepath)


if __name__ == '__main__':
    sys.exit(main())
