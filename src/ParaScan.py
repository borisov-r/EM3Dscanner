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


class ScanObject:
    """
    ScanObject is the main class that creates object
    with given dimensions for scan.

    Returns: servermanager.Fetch( Wavelet() object )

    Methods:
        .RepresentsInt()            # check if input data is integer
        .setDimensions()            # set array dimensions for measurement
        .getDimensions()            # get array dimensions for measurement
        .fetchData()                # gets data from the server
        .setScalarName(name)        # set array name
        .getScalarName()            # get array name

    How to work with this class:
        createdObject(waveletProxy) -> createdObject.setDimensions() ->
        -> createdObject.getDimensions() -> createdObject.fetchData() ->
        -> createdObject.toCellData() -> createdObject.writeToPVDFile()
    """
    def __init__(self, proxyToWavelet):
        self.zero = 0
        self.one = 1
        self.obj = proxyToWavelet
        self.fetchedObj = None
        self.cellData = None

    def RepresentsInt(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def setDimensions(self, x=None, y=None, z=None):
        """
        Set dimensions of Wavelet() object for scan.
        This is the points that will be scanned: 100 x 100 x 10 = 100000 points
        For simplicity we will work in I quadrant this means only positive
        values for x, y and z are accepted.
        Returns: True on proper set of dimensions
        Example: .setDimensions() or .setDimensions(10, 10, 10)
        """
        if x is None:
            x = input('Set points to measure X axis: ')
            print x
        if y is None:
            y = input('Set points to measure Y axis: ')
            print y
        if z is None:
            z = input('Set points to measure Z axis: ')
            print z
        # check for integer numbers
        if self.RepresentsInt(x) and self.RepresentsInt(y) and self.RepresentsInt(z):
            self.obj.WholeExtent.SetData([0, x, 0, y, 0, z])
            return True
        else:
            return False

    def getDimensions(self):
        """
        Get dimensions of Wavelet() object for scan
        Rerturns: list of WholeExtent parameters for measurement
        Example: print test.getDimensions()
        """
        return self.obj.WholeExtent.GetData()

    def fetchData(self):
        """
        servermanager.Fetch() from server
        Returns: data object with dimensions specified by .setDimensions method
        """
        self.fetchedObj = servermanager.Fetch(self.obj)
        return self.fetchedObj

    def setScalarName(self, name=None):
        """
        This method should be executed after .fetchData() method.
        Returns: True on correct name set
        """
        if self.fetchedObj is not None and name is not None:
            self.fetchedObj.GetPointData().GetScalars().SetName(name)
            return True
        else:
            return False

    def getScalarName(self, number=None):
        """
        Get Name of the Array from the fetched data.
        Returns: DataArray name
        """
        if self.fetchedObj is not None and number is not None:
            return self.fetchedObj.GetPointData().GetArrayName(number)
        else:
            return False

    def pointDataToCellData(self):
        """
        Makes point data to cell data.
        For our measurements we use cell data !
        Data should be modified after all point data set to zeros.
        Returns: True
        Example:
        """
        if self.fetchedObj is not None:
            self.cellData = servermanager.filters.PointDataToCellData(self.obj)
            return True
        else:
            return False


class Wave(servermanager.sources.Wavelet):
    """
    This is extension of Wavelet() object in paraview for our
    measurement purposes.

    """
    def SetPointDataToZero(self, wavelet):
        """
        SetPointDataToZeros
        wavelet is a proxy to Wavelet() object
        """
        self.Data = servermanager.Fetch(wavelet)
        scalars = self.Data.GetPointData().GetScalars()
        for i in range(scalars.GetNumberOfTuples()):
            scalars.SetComponent(i, 0, 0.0)
        self.Data.UpdatePipeline()


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
    # print parameters of the Wavelet
    print(w.WholeExtent.GetData())
    # set cube dimentent.GetData()
    test = ScanObject(w)
    test.setDimensions()
    print test.getDimensions()
    fetcheddata = test.fetchData()
    test.setScalarName('Amplitude')
    print fetcheddata
    # print DataArray name
    print('DataArray name: ' + test.getScalarName(0))
    view = servermanager.CreateRenderView()
    servermanager.CreateRepresentation(w, view)
    Show()
    RenameSource('MeasuredData')
    Render()


if __name__ == "__main__":
    main()
