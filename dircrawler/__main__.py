#!/usr/bin/env python

import argparse
import sys

from .crawl import DirCrawler
from .structures import FileStatus


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
    """Main method"""
    options = handle_args()
    dircrawler = DirCrawler(options.directory, progress=options.progress,
                            snapshot_file=options.snapshot_file,
                            snapshot_handler=options.snapshot_handler)
    for filepath, status, transformed in dircrawler.traverse(transformer=options.transformer):
        if status == FileStatus.UNCHANGED:
            continue
        print "%s\t%s\t%s" % (status, transformed, filepath)


if __name__ == '__main__':
    sys.exit(main())
