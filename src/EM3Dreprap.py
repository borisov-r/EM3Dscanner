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

Basic functions that should be implemented:
    - create Wavelet() with arbitrary dimensions X, Y, Z
    - change PointData to CellData and work with CellData
    - save measured data to file
    - add / remove DataArray() to / from measured data

Simple example:

"""
# define path to pyserial here
import sys
sys.path.append('/usr/lib/python2.7/dist-packages')
from serial import Serial


class RepRap(object):
    """ Main class for communication and control of RepRap.
    """
    def __init__(self, baudRate):
        timeout = 5
        self.baud = baudRate
        self.port = self.testPortsForRepRap()
        print("Found RepRap on port: ")
        print(self.port)
        if ("ACM" in self.port):
            self.printer = Serial(self.port, self.baud, timeout)
            #without these readout nothing moves ??? strange but true
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print(self.printer.readline().strip())
            print("send: G91")
            word = 'G91\r\n'
            self.printer.write(word)
            print(self.printer.readline().strip())

    def scanForSerialPorts(self):
        """scan for available ports.
        return a list of device names.
        """
        baselist = []
        if os.name == "nt":
            try:
                import winreg   # @UnresolvedImport
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     "HARDWARE\\DEVICEMAP\\SERIALCOMM")
                i = 0
                while(1):
                    baselist += [winreg.EnumValue(key, i)[1]]
                    i += 1
            except:
                pass
        if os.name == "posix":
            pass

        return baselist + glob.glob("/dev/ttyUSB*")
        + glob.glob("/dev/ttyACM*")
        + glob.glob("/dev/tty.*")
        + glob.glob("/dev/cu.*")
        + glob.glob("/dev/rfcomm*")

    def testPortsForRepRap(self):
        """ Test found available port from scanserial() function
        returns 'port name' or 'none'
        """
        # port that will be used for communication with RepRap
        self.portOk = "none"
        portName = self.scanForSerialPorts()
        num = len(portName)
        try:
            for portName[num - 1] in portName:
                printer = Serial(portName[num - 1], 115200, timeout=30)
                answer = printer.readline().strip()
                printer.close()
                #print(answer.decode('ascii'))
                if ("Sprinter" in answer.decode('ascii')):
                    self.portOk = portName[num - 1]
                    if self.debug:
                        print("OK port is: ", self.portOk)
                    else:
                        pass
                else:
                    pass
        except:
            print("Something happend, don't know yet.")

        if self.portOk is not "none":
            return self.portOk
        else:
            return self.portOk
            print("Port not found.")

    def disconnect(self):
        """ Disconnect from RepRap.
        """
        try:
            self.printer.close()
            print("RepRap printer is now disconnected.")
        except:
            print("RepRap is not connected")

    def checkForValidAxis(self, axis):
        """ Checks input parameters for the movement
        Returns True or False.
        """
        allowed = ["X", "Y", "Z", "E"]
        if axis in allowed:
            return True
        else:
            return False

    def checkForValidDirection(self, direction):
        """ Checks input parameters for the direction
        Returns True or False.
        """
        allowed = ["+", "-"]
        if direction in allowed:
            return True
        else:
            return False

    def move(self, axis, direction, value, speed):
        """ Moves given
        'axis' in '+' or '-' 'direction' with 'value' and 'speed'

        Example: printer.move("X", "+", 15, 50)
        """
        word = None
        moveAxis = None
        moveDirection = None
        #
        if self.checkForValidAxis(axis):
            moveAxis = axis
        else:
            print("Axis definition Error. Please enter \"X\", \"Y\", \"Z\", \"E\".")
        #
        if self.checkForValidDirection(direction):
            moveDirection = direction
        else:
            print("Direction definition Error. Please enter \"+\", \"-\".")
        #
        if moveAxis is not None and moveDirection is not None:
            word = "G1 " + moveAxis + moveDirection
            + str(value) + " F" + str(speed) + "\r\n"
        #
        return word
