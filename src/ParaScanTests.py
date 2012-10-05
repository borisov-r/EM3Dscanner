#!/usr/bin/env python

#==============================================================================
# ParaScanTests is part of ParaScan suit software.
#
# ParaScan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ParaScan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Printrun. If not, see <http://www.gnu.org/licenses/>
#==============================================================================

"""ParaScanTests is a module for testing the functions that are implemented in
ParaScan module. ParaScanTests run from bash with pvpython, which is ParaView's
python module. In order to run tests properly a path to the folder containing
ParaScan ana ParaScanTests modules should be appended to python.

A simple example:
    # update the path to be folder containing ParaScan.py file
    sys.path.append('/home/borisov-r/git/3DEMscanner/src')

    from ParaScan import *

    # run tests from bash
    root@borisov-r:~$ cd ParaView-3.14.0-Linux-64bit/bin
    root@borisov-r:~$ ./pvpython ~/git/3DEMscanner/src/ParaScanTests.py

    # the result should look like this
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK
    root@borisov-r:~$
"""

import unittest
import sys
# append the working directory path
sys.path.append("/home/borisov-r/git/3DEMscanner/src")

from ParaScan import *


class LogToFileTests(unittest.TestCase):
    """
    Test for LogToFile class methods
    """
    def setUp(self):
        self.log = LogToFile('parascan', 'log/parascanTests.log')

    def testLoggingToFile(self):
        self.assertTrue(self.log.name is not None)

    def testLoggingToFileFail(self):
        self.assertFalse(self.log.name is None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
