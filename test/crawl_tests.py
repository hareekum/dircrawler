import os

from datetime import datetime
import shutil

from pyfakefs import fake_filesystem_unittest
from freezegun import freeze_time
from dircrawler.crawl import DirCrawler
from dircrawler.structures import FileStatus
from dircrawler.utils import datetime_to_timestamp


class CrawlTests(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs('/foo/dir')
        os.makedirs('/snapshots')
        self.snapshot_time = '2016-04-10 12:00:01'
        self.files_and_mtimes = {
            '/foo/file1': '2016-05-10 12:00:01',  # > snapshot time
            '/foo/dir/file2': '2016-06-10 12:00:01',  # > snapshot time
            '/foo/dir/file3': '2016-02-10 12:00:01',  # < snapshot time
            '/foo/dir/file4': '2016-04-10 12:00:01'  # = snapshot time
        }
        self.additional_files_and_mtimes = {
            '/foo/dir/file5': '2016-05-10 12:00:01'
        }
        for filepath, mtime in self.files_and_mtimes.iteritems():
            with freeze_time(mtime):
                with open(filepath, 'w') as fh:
                    fh.write('some text')

        for filepath, mtime in self.additional_files_and_mtimes.iteritems():
            with freeze_time(mtime):
                with open(filepath, 'w') as fh:
                    fh.write('some text')

    def tearDown(self):
        shutil.rmtree('/foo')
        shutil.rmtree('/snapshots')
        self.tearDownPyfakefs()

    def test_crawl_without_snapshots_or_transformers(self):
        dc = DirCrawler('/foo')
        for filename, state, transformed in dc.traverse():
            self.assertEquals(FileStatus.ADDED, state)  # all files are ADDED with no snapshot

    def test_crawl_with_snapshot(self):
        snapshot_file = '/snapshots/snapshots.dump'
        with open(snapshot_file, 'w') as fh:
            for filepath in self.files_and_mtimes:
                dt = datetime.strptime(self.snapshot_time, '%Y-%m-%d %H:%M:%S')
                fh.write('%s %s\n' % (filepath, datetime_to_timestamp(dt)))
            fh.write('/foo/dir/file6 %s\n' % datetime_to_timestamp(datetime.now()))  # removed file

        dc = DirCrawler('/foo', snapshot_file=snapshot_file,
                        snapshot_handler='dircrawler.snapshot_handlers.WhiteSpaceSeparatedSnapshotHandler')
        expected_status = {
            '/foo/file1': FileStatus.MODIFIED,
            '/foo/dir/file2': FileStatus.MODIFIED,
            '/foo/dir/file3': FileStatus.UNKNOWN,
            '/foo/dir/file4': FileStatus.UNCHANGED,
            '/foo/dir/file5': FileStatus.ADDED,
            '/foo/dir/file6': FileStatus.REMOVED,
        }
        for filepath, status, transformed in dc.traverse():
            self.assertEquals(status, expected_status[filepath])

    def test_crawl_with_transformer(self):
        dc = DirCrawler('/foo')
        for filepath, status, transformed in dc.traverse(
                transformer='dircrawler.transformers.FirstLineTransformer'):
            self.assertEquals('some text', transformed)
