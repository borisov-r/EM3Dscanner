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

""" Filename: EM3Dreprap.py

EM3Dscanner is a macro for ParaView for automation of measurement process of EM
waves with RepRap, Probe, PNA and ParaView
The scanner consists of:

    * Probe     - different probes are used for E and H vector of EM field
    * RepRap    - control the movement of the 'probe'
    * PNA       - measurements using Agilent N5230C Network Analyzer
    * ParaView  - data visualization software

Official web site: https://github.com/borisov-r/3DEMscanner/wiki

Usage:
    reprap = RepRap()
    reprap.connect("/dev/ttyACM0", 115200)
    measureTuple = (0, 4, 0, 4, 0, 2)
    reprap.setMeasureDimensions(measureTuple)
    reprap.moveOneCube(wavelet=None, pna=None)
    reprap.disconnect()
"""
import sys
sys.path.append('/usr/lib/python2.7/dist-packages')
from serial import Serial
from time import sleep


class RepRap(object):
    """ Communication with reprap.
    """
    def __init__(self):
        self.term = '\r\n'
        self.port = None
        self.baudrate = None
        self.printer = None
        self.xPoints = None
        self.yPoints = None
        self.zPoints = None
        self.currentPoint = None

    def connect(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        try:
            self.printer = Serial(self.port, self.baudrate)
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.write('G91' + self.term)
            return True
        except:
            print 'Error while connecting to printer.'

    def setX(self, minusX, plusX):
        self.x = abs(minusX) + abs(plusX)

    def getX(self):
        return self.x

    def setY(self, minusY, plusY):
        self.y = abs(minusY) + abs(plusY)

    def getY(self):
        return self.y

    def setZ(self, minusZ, plusZ):
        self.z = abs(minusZ) + abs(plusZ)

    def getZ(self):
        return self.z

    def getCurrentCoordinates(self):
        ''' Get current printer position and
            return value in format:
                SENDING:M114
                X:0.00Y:0.00Z:0.00E:0.00
        '''
        if self.printer is not None:
            self.printer.write('M114' + self.term)
            self.readline().strip()
            return self.readline().strip()

    def setMeasureDimensions(self, dimensionsTuple):
        self.setX(dimensionsTuple[0], dimensionsTuple[1])
        self.setY(dimensionsTuple[2], dimensionsTuple[3])
        self.setZ(dimensionsTuple[4], dimensionsTuple[5])

    def getNumberOfMeasurePoints(self):
        points = self.x * self.y * self.z
        return points

    def disconnect(self):
        if self.printer is not None:
            try:
                self.printer.close()
            except:
                print 'Error while disconnecting.'
        else:
            print 'Already disconnected.'

    def move(self, ff=True, moveX=0, moveY=0, moveZ=0, speed=400, wait=False,
             waitAtPointTime=1):
        """ Move reprap with default speed 100 mm/min.
        ff is parameter that defines the movement direction.
            True - forward (+ direction)
            False - backwards (- direction)
        """
        if ff:
            sign = '+'
        else:
            sign = '-'
        if self.printer is not None:
            self.printer.write('G91' + self.term)
            self.printer.readline().strip()
            word = 'G1 X' + sign + str(moveX) + ' Y' + sign + str(moveY) + ' Z'
            + sign + str(moveZ) + ' F' + str(speed)
            self.printer.write(word + self.term)
            # sleep(waitAtPointTime)
            self.movement = None
            # print self.movement
            while True:
                self.movement = self.printer.readline().strip()
                if ("Movement finished." in self.movement):
                    break
            if wait:
                word = 'M400' + self.term
                self.printer.write(word)
                self.printer.readline().strip()
        else:
            print 'Check printer connection.'

    def moveOneSlice(self, wavelet=None, pna=None, yDirection=True, z=0,
                     resolution=1):
        """ Move one slice X and Y.
        """
        for y in range(self.y):
            for x in range(self.x):
                # check if y is odd or even
                if y & 1:   # y is odd
                    self.move(False, resolution)
                    if z & 1:
                        yData = (self.y - 1) - y
                        xData = (self.x - 1) - x
                    else:
                        yData = y
                        xData = (self.x - 1) - x
                else:       # y is even
                    self.move(True, resolution)
                    if z & 1:
                        yData = (self.y - 1) - y
                        xData = x
                    else:
                        yData = y
                        xData = x
                    #yData = y
                print 'X is: ', xData, "; Y is: ", yData, "; Z is: ", z
                if wavelet is not None:
                    if pna is not None:
                        dim = wavelet.dimensions
                        if "N5230C" in pna.IDN:
                            #dim = wavelet.dimensions
                            #print 'Wavelet dimensions: ' + dim
                            print 'Data received from PNA.'
                            print pna.IDN
                            #if "N5230C" is in pna.IDN:
                            data = pna.askPna('calc:data? fdata')
                        elif "rfAtmega128" in pna.IDN:
                            pna.readRSSI()
                            data = pna.msg
                            pna.clearRSSIbuffer()
                    else:
                        print "Measurement equipment not found."
                    #fill the data if measurement equipment found.
                    if pna.IDN is not None:
                        splitData = data.split(',')
                        print splitData
                        print "X point: ", dim[0] + xData, "; Y point: ",
                        dim[2] + yData, "; Z point: ", dim[4] + z
                        # set correct absolute coordinates of measured point in
                        # wavelet object.
                        wavelet.SetCellData(splitData[0],
                                            dim[0] + xData,     # set corrected x coordinate
                                            dim[2] + yData,     # set corrected y coordinate
                                            dim[4] + z)     # set corrected z coordinate
                    else:
                        print "No available data from measurement equipment."
            # move y direction and stop at last point
            if y != self.y - 1:         # this makes the y to stop at the end
                self.move(yDirection, 0, resolution)

    def moveOneCube(self, wavelet=None, pna=None, resolution=1):
        """ Measure one cube.
        """
        for z in range(self.z):
            # check if z is odd or even
            if z & 1:   # z is odd
                self.moveOneSlice(wavelet, pna, False, z)
            else:       # z is even
                self.moveOneSlice(wavelet, pna, True, z)
            # stop z at last point, else move
            if z != self.z - 1:     # this makes the z to stop at last point
                self.move(True, 0, 0, resolution)


def main():
    reprap = RepRap()
    reprap.connect('/dev/ttyACM0', 115200)
    expTuple = (-3, 3, 0, -6, 2, -2)
    print 'Test tuple of points for measurement: ',
    print expTuple
    reprap.setMeasureDimensions(expTuple)
    print 'Points to measure X: ',
    print reprap.getX()
    print 'Points to measure Y: ',
    print reprap.getY()
    print 'Points to measure Z: ',
    print reprap.getZ()
    reprap.moveOneCube()


if __name__ == '__main__':
    main()
