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


###############################################################################
# create Wavelet() object
wave = Wavelet()

# change dimensions of the cube (points to measure)
minusX = input("Enter value for -X: ")
print(minusX)
plusX = input("Enter value for X: ")
print(plusX)

minusY = input("Enter value for -Y: ")
print(minusY)
plusY = input("Enter value for Y: ")
print(plusY)

minusZ = input("Enter value for -Z: ")
print(minusZ)
plusZ = input("Enter value for Z: ")
print(plusZ)

wave.WholeExtent.SetData([minusX, plusX, minusY, plusY, minusZ, plusZ])

cellWave = PointDatatoCellData(wave)

fetchCellWave = servermanager.Fetch(cellWave)

fetchCellWave.GetCellData().GetScalars().SetName("Amplitude")
for i in range(int(fetchCellWave.GetCellData().GetScalars().GetNumberOfTuples())):
            fetchCellWave.GetCellData().GetScalars().SetComponent(i, 0, 0.0)

cellWave.UpdatePipeline()

RenameSource("Measurement")

# <paraview.servermanager.UniformGridRepresentation object at
# 0x3f32f50>
fetchCellWave.GetCellData().GetScalars().SetComponent(0, 0, 255.0)
fetchCellWave.GetCellData().GetScalars().SetComponent(999, 0, 255.0)
fetchCellWave.GetCellData().GetScalars().SetComponent(998, 0, 125.0)
cellWave.UpdatePipeline()

Show()
Render()
###############################################################################


pna = NetworkAnalyzer("10.1.15.106", "5024")

if pna.connect() is True:
    print("Connected to PNA.")
    pna.send("*IDN?")
    print pna.receive()
    #
    pna.send("mmem:cdir?")
    print("Current working folder: ")
    print pna.receive()
    #
    pna.send("mmem:load 'calibrationRado.csa'")
    print("Load default displays and calibration.")
    print pna.receive()
    #
    pna.send("calc:par:cat?")
    print("Names and parameters of existing measurements for the specified channel:")
    print pna.receive()
    #
    pna.send("format:data ascii")
    pna.send("calc:par:mnum 1")
    # print("format of the stored snp: ")
    pna.send("mmem:stor:trace:format:snp?")
    print("Data format type: ")
    print pna.receive()
    pna.send("mmem:stor:trace:format:snp db")
    pna.send("calc:data? fdata")
    data = pna.receive()
    print("Data received from PNA.")
    print data

if pna.disconnect() is True:
    print("Disconnected from PNA.")
