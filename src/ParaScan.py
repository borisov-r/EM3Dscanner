#!/usr/bin/env python

#==============================================================================
# ParaScan is part of ParaScan suit software.
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


class LogToFile:
    """
    LogToFile creates file with given name
    and make log of the program execution.

        example: LogToFile('parascan', 'parascan_conn.log')

    """
    def __init__(self, loggerName, fileName):
        self.loggerName = loggerName
        self.fileName = fileName
        self.name = getLogger(loggerName)
        # creat log file
        self.loggingToFile(fileName)

    def loggingToFile(self, fileName):
        """
        Creates file with name 'fileName' and logs in format:
            time - name - level - message
            2012-10-05 14:27:17,563 - parascan - INFO - start.
        """
        self.fileName = fileName
        self.name.setLevel(DEBUG)
        fileHandler = FileHandler(self.fileName)
        fileHandler.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.name.addHandler(fileHandler)


def main():
    # creates connection to the server
    logConnection = LogToFile('parascan', 'log/parascanConnection.log')
    logObjects = LogToFile('object', 'log/parascanObject.log')
    print logConnection.name
    logConnection.name.info('Start')
    try:
        connection = servermanager.ActiveConnection
        logConnection.name.info('Successfully connected: %s', connection)
    except:
        logConnection.name.info('Server not found.')
    # create wavelet object
    try:
        w = servermanager.sources.Wavelet()
        logConnection.name.info('Wavelet created successfully.')
    except:
        logConnection.name.info('Error in wavelet creation')
    # end of the program
    logConnection.name.info('End')
    # fetch data from servermanager
    wave = servermanager.Fetch(w)
    logObjects.name.info('Wavelet generated: %s', wave)


if __name__ == "__main__":
    main()
