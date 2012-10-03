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

from logging import *
from paraview import simple
from paraview import servermanager
from paraview import vtk


class SimpleTestClass:

    def __init__(self, trueOrFalse):
        self.tORf = trueOrFalse

    def printWave(self):
        self.wave = simple.Wavelet()
        self.fetchedWave = servermanager.Fetch(self.wave)
        print self.fetchedWave
