import os

from datetime import datetime

from pyfakefs import fake_filesystem_unittest
from freezegun import freeze_time
from dircrawler.utils import datetime_to_timestamp
from dircrawler import snapshot_handlers as handlers


class SnapshotHandlersTests(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs('/foo/dir')
        os.makedirs('/snapshots')
        self.files_and_mtimes = {
            '/foo/file1': '2016-05-10 12:00:01',
            '/foo/dir/file2': '2016-06-10 12:00:01'
        }
        for filepath, mtime in self.files_and_mtimes.iteritems():
            with freeze_time(mtime):
                with open(filepath, 'w') as fh:
                    fh.write('some text')

    def tearDown(self):
        self.tearDownPyfakefs()

    def test_whitespace_separated_file_handling(self):
        snapshot_file = '/snapshots/123.dump'
        with open(snapshot_file, 'w') as fh:
            for filepath, mtime in self.files_and_mtimes.iteritems():
                dt = datetime.strptime(mtime, '%Y-%m-%d %H:%M:%S')
                fh.write('%s %s\n' % (filepath, datetime_to_timestamp(dt)))

        handler = handlers.WhiteSpaceSeparatedSnapshotHandler()
        self.assertEquals(datetime.strptime('2016-05-10 12:00:01', '%Y-%m-%d %H:%M:%S'),
                          list(handler.parse(snapshot_file))[1][1].mod_ts)
