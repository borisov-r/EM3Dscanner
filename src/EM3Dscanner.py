#!/usr/bin/env python

#==============================================================================
# 3DEMscanner.py is part of 3DEMscanner suit software.
#
# 3DEMscanner is free software: you can redistribute it and/or modify
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

""" Filename: EM3Dscanner.py

EM3Dscanner is a macro for ParaView for automation of measurement process of EM
waves with RepRap, Probe, PNA and ParaView
The scanner consists of:

    * Probe     - different probes are used for E and H vector of EM field
    * RepRap    - control the movement of the 'probe'
    * PNA       - measurements using Agilent N5230C Network Analyzer
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
import sys
sys.path.append('/home/borisov-r/git/EM3Dscanner/src')
from paraview import vtk
from EM3Dnalib import NetworkAnalyzer


class MyWavelet:
    """ Initialize Wavelet() object with given dimensions
        and zeros as component values in the array.
        - Array name is set to 'Amplitude'
        - Rename Source to 'Measurement'
    """
    def __init__(self):
        self.zero = 0                    # my zero in this class
        self.wave = Wavelet()
        # set dimensions manually
        # change dimensions of the cube (points to measure)
        #
        minusX = input("Enter value for -X: ")
        print(minusX)
        plusX = input("Enter value for X: ")
        print(plusX)
        #
        minusY = input("Enter value for -Y: ")
        print(minusY)
        plusY = input("Enter value for Y: ")
        print(plusY)
        #
        minusZ = input("Enter value for -Z: ")
        print(minusZ)
        plusZ = input("Enter value for Z: ")
        print(plusZ)
        #
        self.wave.WholeExtent.SetData([minusX, plusX,
                                       minusY, plusY,
                                       minusZ, plusZ])
        # store dimensions in a tuple for later use
        self.dimensions = (minusX, plusX,
                           minusY, plusY,
                           minusZ, plusZ)
        #
        self.wave.Maximum = self.zero
        self.wave.XFreq = self.zero
        self.wave.YFreq = self.zero
        self.wave.ZFreq = self.zero
        self.wave.XMag = self.zero
        self.wave.YMag = self.zero
        self.wave.ZMag = self.zero
        self.wave.StandardDeviation = 0.5
        # this should stay like this StandardDeviation = 0.5 !
        # if StandardDeviation = 0 first element is NaN
        # and script is not working correctly

    def SetPointDataToCellData(self):
        """ Make PointDataToCellData from generated Wavelet()
        Measurements are taken for CellData.
        Returns fetched data from the server.
        """
        # make PointData to CellData
        self.cellWave = PointDatatoCellData(self.wave)
        # fetch Data from the server
        self.fetchedCellWave = servermanager.Fetch(self.cellWave)
        self.fetchedCellWave.GetCellData().GetScalars().SetName("Amplitude")
        RenameSource("Measurement")
        return self.fetchedCellWave

    def GetCellId(self, coordX, coordY, coordZ):
        """ Get CellID from coordinates in the volume.
        """
        # type(fetchCellWave) -> vtkImageData ->
        # -> fetcellCecellWave.ComputeCellId([9, 9, 9])
        id = self.fetchedCellWave.ComputeCellId([coordX, coordY, coordZ])
        return id

    def SetCellData(self, value, coordX, coordY, coordZ):
        """ Set CellData with 'value' to given cell, which is determined
            by its unique coordinates: coordX, coordY, coordZ
        """
        pointID = self.GetCellId(coordX, coordY, coordZ)
        setPoint = self.fetchedCellWave.GetCellData().GetScalars()
        setPoint.SetComponent(pointID, self.zero, float(value))
        self.cellWave.UpdatePipeline()

    def WriteToPVDFile(self, dataMode, name):
        """
        Write data to .pvd file.
        # The mode uses for writing the file's data i.e.
        # ascii = 0, binary = 1, appended binary = 2.
        example: WriteToPVDFile(0, 'test.pvd')
        """
        writer = servermanager.writers.XMLPVDWriter(FileName=name, DataMode=dataMode)
        writer.Input = GetActiveSource()
        writer.UpdatePipeline()
        return True

    def ShowAndRender(self):
        """ Calls Show() and Render() methods in ParaView
        """
        Show()
        Render()


wave = MyWavelet()
wave.SetPointDataToCellData()
pna = NetworkAnalyzer("10.1.15.106", "5024")

if pna.connect() is True:
    pna.send("*IDN?")
    print pna.receive()
    #
    print("Current working folder: ")
    print pna.askPna("mmem:cdir?")
    #
    print("Load default displays and calibration.")
    pna.askPna("mmem:load 'calibrationRado.csa'")
    #
    print("Names and parameters of existing measurements for the specified channel:")
    print pna.askPna("calc:par:cat?")
    #
    # set data from pna to be ascii
    pna.askPna("format:data ascii")
    # set receive data to S11
    pna.askPna("calc:par:mnum 1")
    #
    print("Data format type: ")
    print pna.askPna("mmem:stor:trace:format:snp?")
    #
    print("Set format data to dB")
    pna.askPna("mmem:stor:trace:format:snp db")
    # receive data
    print("Data received from PNA.")
    data = pna.askPna("calc:data? fdata")
    splitData = data.split(",")
    print splitData
    # set first frequency point from pna to X-0, Y-0, Z-0
    wave.SetCellData(splitData[0], 0, 0, 0)
    # set second frequency point from pna to X-0, Y-0, Z-0
    wave.SetCellData(splitData[1], 9, 0, 0)

if pna.disconnect() is True:
    print("Disconnected from PNA.")

wave.ShowAndRender()
print wave.dimensions
wave.WriteToPVDFile(0, "testPVD/myFirstPVD")
