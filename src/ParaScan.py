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

"""ParaScan is the main module of 3DEMscanner suit, that controls the work of
the electromagnetic scanner. The scanner consists of:

    * reprap    - control the movement of the 'probe'
    * pna       - measurements using Agilent N5230C Network Analyzer
    * ParaView  - data visualization software

Official web site: https://github.com/borisov-r/3DEMscanner/wiki

Basic functions that should be implemented:
    - create Wavelet() with arbitrary dimensions X, Y, Z
    - change PointData to CellData and work with CellData
    - save measured data to file
    - add / remove DataArray() to / from measured data

A simple example:
    # create Wavelet object



"""

from logging import *
from paraview import simple
from paraview import servermanager
from paraview import vtk


class ConnectToBIServer:
    """
    Connect is used to create a new session.
    On success it returns a vtkSMSession object that abstracts the
    connection. Otherwise it, returns None.

    We use the simplest connection to built-in server.
    """
    def __init__(self):
        """
        Creates connection to built-in server.
        """
        # start file to log
        self.log = getLogger('parascan')
        # creat log file
        self.loggingToFile('paraTest.log')
        self.log.info('start.')

        # creates connection to the server
        #servermanager.Connect()

        self.log.info('Active connection: ')

    def loggingToFile(self, fileName):
        """
        Creates file with name 'fileName' and logs
        """
        self.fileName = fileName
        self.log.setLevel(DEBUG)
        fileHandler = FileHandler(self.fileName)
        fileHandler.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.log.addHandler(fileHandler)
