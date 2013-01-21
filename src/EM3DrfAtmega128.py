#!/usr/bin/env python

#==============================================================================
# 3DEMnalib.py is part of 3DEMscanner suit software.
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

""" Filename: EM3Dnalib.py

3DEMscanner is a macro for ParaView for automation of measurement process of EM
waves with RepRap, Probe, PNA and ParaView
The scanner consists of:

    * Probe     - different probes are used for E and H vector of EM field
    * RepRap    - control the movement of the 'Probe'
    * PNA       - measurements using Agilent N5230C Network Analyzer
    * ParaView  - data visualization software

Official web site: https://github.com/borisov-r/3DEMscanner/wiki

    nalib  is the basic library used to communicate with Agilent N5230C PNA.

Main class is called 'NetworkAnalyzer' and consists of following methods:
    - __init__("10.1.15.106", "5024")
    - connect()     # return True on success
    - disconnect()  # return True on success
    - send('message')
    - receive()
    - receiveError()    # check if Error in PNA buffer
"""
import sys
sys.path.append('/usr/lib/python2.7/dist-packages')
from serial import Serial
# from time import sleep


class RfAtmega128(object):
    """ Communication with rfAtmega128 board
        with Spectrum Analyzer firmware
    """
    def __init__(self):
        self.IDN = None         # set device to rfAtmega128
        self.term = '\r\n'
        self.port = None
        self.baudrate = None
        self.rfAtmega = None
        self.msg = None

    def connect(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        try:
            self.rfAtmega = Serial(self.port, self.baudrate, timeout=1)
            self.rfAtmega.write('wa' + self.term)
            # flush the buffer of ATmega128rfa1
            # otherwise can't start reading the data
            self.msg = self.rfAtmega.readline().strip()
            self.msg = self.rfAtmega.readline().strip()
            self.msg = self.rfAtmega.readline().strip()
            self.msg = self.rfAtmega.readline().strip()
            self.IDN = "rfAtmega128"
            return True
        except:
            print 'Error while connecting to rfAtmega128 board.'

    def disconnect(self):
        if self.rfAtmega is not None:
            try:
                self.rfAtmega.close()
                return True
            except:
                print 'Error while disconnecting.'
        else:
            print 'Already disconnected.'

    def readRSSI(self):
        if self.rfAtmega is not None:
            #self.rfAtmega.write("w\r\n")
            self.msg = self.rfAtmega.readline().strip()
            self.msg = self.rfAtmega.readline().strip()
            self.msg = self.rfAtmega.readline().strip()
            self.msg = self.rfAtmega.readline().strip()
        else:
            print 'Error receiving RSSI.'


def main():
    rfAtmega = RfAtmega128()
    rfAtmega.connect('/dev/ttyUSB0', 9600)
    rfAtmega.readRSSI()
    print rfAtmega.msg
    rfAtmega.readRSSI()
    print rfAtmega.msg
    rfAtmega.readRSSI()
    print rfAtmega.msg
    rfAtmega.readRSSI()
    print rfAtmega.msg
    rfAtmega.disconnect()

if __name__ == "__main__":
    main()
