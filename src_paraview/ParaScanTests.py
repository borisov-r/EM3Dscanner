"""simple is a module for using paraview server manager in Python. It
provides a simple convenience layer to functionality provided by the
C++ classes wrapped to Python as well as the servermanager module.

A simple example:
  from paraview.simple import *

  # Create a new sphere proxy on the active connection and register it
  # in the sources group.
  sphere = Sphere(ThetaResolution=16, PhiResolution=32)

  # Apply a shrink filter
  shrink = Shrink(sphere)

  # Turn the visiblity of the shrink object on.
  Show(shrink)

  # Render the scene
  Render()
"""
#==============================================================================
#
#  Program:   ParaView
#  Module:    simple.py
#
#  Copyright (c) Kitware, Inc.
#  All rights reserved.
#  See Copyright.txt or http://www.paraview.org/HTML/Copyright.html for details.
#
#     This software is distributed WITHOUT ANY WARRANTY; without even
#     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the above copyright notice for more information.
#
#==============================================================================

import unittest
import sys
# append the working directory path
sys.path.append("/home/borisov-r/git/3DEMscanner/src_paraview")

from ParaScan import *


class ParaScanTests(unittest.TestCase):
    """A class whose methods are test cases.

    By default this class initialize a Wavelet() object in ParaView

    All tests should be run from ParaView python interpreter for now.
    """
    def setUp(self):
        self.st = SimpleTestClass(True)
        self.trueOrFalse = self.st.tORf

    def testTrue(self):
        # self.st.printWave()
        self.assertTrue(self.trueOrFalse)

    def testFalse(self):
        # self.st.printWave()
        self.assertFalse(self.trueOrFalse and False)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
