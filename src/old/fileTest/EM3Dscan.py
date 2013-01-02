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

""" Filename: EM3Dscan.py

EM3Dscanner is a macro for ParaView for automation of measurement process of EM
waves with RepRap, Probe, PNA and ParaView
The scanner consists of:

    * Probe     - different probes are used for E and H vector of EM field
    * RepRap    - control the movement of the 'probe'
    * PNA       - measurements using Agilent N5230C Network Analyzer
    * ParaView  - data visualization software

Official web site: https://github.com/borisov-r/3DEMscanner/wiki

Usage:
"""


class GetDimensionsTuple:
    """ This class is used to get the input for the measurement dimenssions
        and returns a list of the values for MyWavelet class.

        This is test class for now to so I can try
        GroupDatasets( Input=[ Measurement1, Measurement2 ] ) filter.
    """
    def __init__(self):
        # set dimensions manually
        # change dimensions of the cube (points to measure)
        #
        self.minusX = input("Enter value for -X: ")
        print(self.minusX)
        self.plusX = input("Enter value for X: ")
        print(self.plusX)
        #
        self.minusY = input("Enter value for -Y: ")
        print(self.minusY)
        self.plusY = input("Enter value for Y: ")
        print(self.plusY)
        #
        self.minusZ = input("Enter value for -Z: ")
        print(self.minusZ)
        self.plusZ = input("Enter value for Z: ")
        print(self.plusZ)

    def GetDimensions(self):
        """ return dimensions to be measured
        """
        return (self.minusX, self.plusX,
                self.minusY, self.plusY,
                self.minusZ, self.plusZ)


class GenerateDataFile(object):
    """ Main class that collects data from PNA and puts data to files
        for paraview as image arrays.
    """
    def __init__(self, reprapObject=None, pnaObject=None):
        self.reprap = reprapObject      # reference to reprap
        self.pna = pnaObject            # reference to pna
        self.fileHeader = None
        self.fileFooter = None

    def setFile(self, fileName="msr", extent=(0, 0, 0, 0, 0, 0),
                index=0, freq=None, dataArrayName=None):
        """ File header is defined from Tuple with dimensions from
        GetDimensionsTuple.GetDimensions(), index, freq and dataArrayName:
            * index - is file index '_0' (range: from 0 to 2000)
                      this parameter is dependent from pna's measurement points.
            * freq  - is the measurement frequency from pna and
                      will define the Scalars in the file.
            * dataArrayName - is the measured parameter Amplitude or Phase.
        """
        if freq is not None:
            fileName = fileName + "_" + str(index)
            file = open(fileName, "w")
            file.write('<VTKFile type="ImageData" version="0.1" byte_order="LittleEndian">\r\n')
            file.write('  <ImageData WholeExtent="')
            wholeExtent1 = str(extent[0]) + ", " + str(extent[1]) + ", "
            wholeExtent2 = str(extent[2]) + ", " + str(extent[3]) + ", "
            wholeExtent3 = str(extent[4]) + ", " + str(extent[5])
            wholeExtent = wholeExtent1 + wholeExtent2 + wholeExtent3
            file.write(wholeExtent)
            file.write('" Origin="0 0 0" Spacing="1 1 1">\r\n')
            file.write('  <Piece Extent="' + wholeExtent + '"\r\n')
            file.write('    <PointData>\r\n')
            file.write('    </PointData>\r\n')
            file.write('    <CellData Scalars="' + str(freq) + '">\r\n')
            file.write('    <DataArray type="Float32" Name="' + str(dataArrayName)
                       + '" format="ascii" RangeMin="-110.0" RangeMax="60">\r\n')
            file.write('    </DataArray>\r\n')
            file.write('    </CellData>\r\n')
            file.write('  </Piece>\r\n')
            file.write('  </ImageData>\r\n')
            file.write('</VTKFile>\r\n')
            file.close()


def main():
    dl = GetDimensionsTuple()
    file = GenerateDataFile()
    file.setFile("testHeader", dl.GetDimensions(), 1, "19.5 GHz", "Phase")

if __name__ == "__main__":
    main()
