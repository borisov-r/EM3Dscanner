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


class ParaScanTests(unittest.TestCase):
    """A class whose methods are test cases.

    By default this class initialize a Wavelet() object in ParaView

    All tests should be run from ParaView python interpreter for now.
    """
    def setUp(self):
        # connect to built-in server
        servermanager.Connect('localhost')
        self.conn = ConnectToBIServer()

    def testConnectToBIServer(self):
        """
        Test if there is a problem with the connection.
        """
        self.assertTrue(self.conn is not None)

    def testConnectToBIServerFail(self):
        """
        Test if the connection fails in certain cases.
        """
        self.assertFalse(self.conn is None)

    def testLoggingToFile(self):
        """
        Write some log to file calling loggingToFile method
        How to check if the log file is created ?
        """
        self.assertTrue(True)

    def testLoggingToFileFail(self):
        """
        Write some log to file calling loggingToFile method
        How to check if the log file is created ?
        """
        self.assertFalse(False)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
