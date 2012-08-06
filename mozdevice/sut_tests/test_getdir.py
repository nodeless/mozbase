# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import tempfile
from dmunit import DeviceManagerTestCase


class GetDirectoryTestCase(DeviceManagerTestCase):

    def _setUp(self):
        self.localsrcdir = tempfile.mkdtemp()
        os.makedirs(self.localsrcdir + '/push1/sub.1/sub.2')
        file(self.localsrcdir + '/push1/sub.1/sub.2/testfile', 'w').close()
        os.makedirs(self.localsrcdir + '/push1/emptysub')
        self.localdestdir = tempfile.mkdtemp()
        self.expected_filelist = ['emptysub', 'sub.1']

    def tearDown(self):
        shutil.rmtree(self.localsrcdir)
        shutil.rmtree(self.localdestdir)

    def runTest(self):
        """This tests the getDirectory() function.
        """
        testroot = self.dm.getDeviceRoot() + '/infratest'
        self.dm.removeDir(testroot)
        self.dm.mkDir(testroot)
        self.dm.pushDir(self.localsrcdir + '/push1', testroot + '/push1')
        # pushDir doesn't copy over empty directories, but we want to make sure that
        # they are retrieved correctly.
        self.dm.mkDir(testroot + '/push1/emptysub')
        filelist = self.dm.getDirectory(testroot + '/push1', self.localdestdir + '/push1')
        filelist.sort()
        self.assertEqual(filelist, self.expected_filelist)
        self.assertTrue(os.path.exists(self.localdestdir + '/push1/sub.1/sub.2/testfile'))
        self.assertTrue(os.path.exists(self.localdestdir + '/push1/emptysub'))
        filelist = self.dm.getDirectory('/doesnotexistatall', self.localdestdir + '/none')
        self.assertEqual(filelist, None)
        self.assertFalse(os.path.exists(self.localdestdir + '/none'))
