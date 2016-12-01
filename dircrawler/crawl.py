import os
import datetime

import progressbar

import utils


class FileStatus(object):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"
    UNKNOWN = "UNKNOWN"


class FileState(object):
    def __init__(self, mod_ts=None):
        self.mod_ts = mod_ts
        self.visited = False


class DirCrawler(object):
    def __init__(self, dirpath, progress=False, snapshot_file=None):
        self.dirpath = dirpath
        self.progress = progress
        self.snapshot = self._parse_snapshot(snapshot_file) if snapshot_file else {}
        self.file_count = self._get_file_count() if self.progress else None

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
        elif utils.mod_ts_in_utc(filepath) > states[filepath].mod_ts:
            states[filepath].visited = True
            return FileStatus.MODIFIED
        else:
            # This should not happen
            return FileStatus.UNKNOWN

    def traverse(self, transform=lambda fp: None):
        """
        Recursively traverses through a directory, computes state of a file,
        applies transformation if specified and returns a tuple of
        (file path, state, transformed output)
        """
        bar = progressbar.ProgressBar(
            widgets=['Progress: ', progressbar.Percentage(), ' | ', progressbar.ETA()],
            max_value=self.file_count, redirect_stdout=True)
        count = 0

        # Walk through all files in dirpath
        for filepath in self._walk_dir():
            yield filepath, self._get_file_state(filepath), transform(filepath)
            bar.update(count)
            count += 1

        # Check for files in snapshot but not in dirpath
        for filepath, state in states.iteritems():
            if not state.visited:
                yield filepath, FileStatus.REMOVED, None


if __name__ == '__main__':
    # states = {}
    # states.update({'/Users/hari/personal/dircrawler/dircrawler/crawl.py': FileState(
    #     mod_ts=datetime.datetime.now())})
    # states.update({'/Users/hari/personal/dircrawler/dircrawler/fake.py': FileState(
    #     mod_ts=datetime.datetime.now())})

    d = DirCrawler('/Users/hari/personal/dircrawler/dircrawler', progress=True, snapshot_file=None)
    for f in d.traverse():
        print f
