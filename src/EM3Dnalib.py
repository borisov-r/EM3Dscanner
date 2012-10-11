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

""" Filename: EM3Dnalib.py

3DEMscanner is a macro for ParaView for automation of measurement process of EM
waves with RepRap, Probe, PNA and ParaView
The scanner consists of:

    * Probe     - different probes are used for E and H vector of EM field
    * RepRap    - control the movement of the 'probe'
    * PNA       - measurements using Agilent N5230C Network Analyzer
    * ParaView  - data visualization software

Official web site: https://github.com/borisov-r/3DEMscanner/wiki

nalib is the basic library used to communicate with Agilent N5230C PNA.

Main class is called 'NetworkAnalyzer' and consists of following methods:
    - __init__("10.1.15.106", "5024")
    - connect()     # return True on success
    - disconnect()  # return True on success
    - send('message')
    - receive()
    - receiveError()    # check if Error in PNA buffer

"""
# telnetlib for communication
from telnetlib import Telnet


class NetworkAnalyzer:
    """ Main class for communication with PNA.

    Example: pna = NetworkAnalyzer("10.1.15.106", "5024")

    Important ! Use " to send IP and Port addresses.
    """
    def __init__(self, IPaddress, Port):
        self.IDN = None             # pna identification
        self.IPaddress = IPaddress  # used IP address of pna
        self.Port = Port            # used telnet port of pna
        self.Timeout = 5            # time to connect to pna
        self.TimeoutShort = 0.5     # shorter time to wait data from pna
        self.TermChar = "\n"        # termination character
        self.ScpiChar = "SCPI> "    # read_until("SCPI> ")
        # ask pna for system error messages
        self.AskForSystemErrorMsg = "SYSTEM:ERROR?"
        self.tn = None

    def connect(self):
        # connect to PNA via telnet
        try:
            if self.tn is None:
                self.tn = Telnet(self.IPaddress, self.Port, self.Timeout)
                self.tn.read_until(self.ScpiChar, self.Timeout)
                self.tn.write("*IDN?")
                self.tn.write(self.TermChar)
                self.IDN = self.tn.read_until(self.TermChar, self.Timeout)
                # flush the pna buffer
                self.tn.read_until(self.ScpiChar, self.Timeout)
                return True
            else:
                print("Already connected to PNA.")
        except:
            print("Error while connecting.")

    def disconnect(self):
        # disconnect telnet connection to pna
        try:
            if self.tn is not None:
                self.tn.close()
                self.IDN = None     # if pna is closed follows no IDN
                return True
            else:
                print("No PNA connection.")
        except:
            print("Error while disconnecting.")

    def send(self, msg):
        """ Send message to PNA.

        Example: tn.send('*IDN?') # returns the identification of the PNA
        """
        try:
            self.tn.write(msg)
            self.tn.write(self.TermChar)
        except:
            print("Error while sending message: %s", msg)

    def receive(self):
        """ Receive message from PNA.

        Example: tn.receive() # gets data from PNA.

        Better implementation:
            1. check if error in PNA (flush error buffer)
            2. then receive data
            3. if error return False, else return message
        """
        try:
            message = self.tn.read_until(self.TermChar, self.TimeoutShort)
            self.tn.read_until(self.ScpiChar, self.TimeoutShort)
            return message.strip()
        except:
            print("Error while 'receive' message from PNA.")

    def receiveError(self):
        """ Check if errors in PNA buffers exist.
        """
        try:
            self.tn.write(self.AskForSystemErrorMsg)
            self.tn.write(self.TermChar)
            message = self.tn.read_until(self.TermChar, self.TimeoutShort)
            # flush pna buffer to be clear
            self.tn.read_until(self.ScpiChar, self.TimeoutShort)
            return message.strip()
        except:
            print("Error while 'receiveError' function called.")

    def askPna(self, message):
        """ Send command to PNA and returns received message.
        """
        try:
            self.send(message)
            return self.receive()
        except:
            print("Error when 'ask' PNA.")


def main():
    pna = NetworkAnalyzer("10.1.15.106", "5024")
    if pna.connect() is True:
        print("Connected to PNA.")
        # print(pna.IDN)
        pna.askPna("*IDN?")
        print pna.receiveError()
        # print("Load default displays and calibration.")
        pna.askPna("mmem:load 'calibrationRado.csa'")
        # print("Names and parameters of existing measurements for the specified channel:")
        print pna.askPna("calc:par:cat?")

    if pna.disconnect() is True:
        print("Disconnected from PNA.")
        print "PNA IDN set to:", pna.IDN


if __name__ == "__main__":
    main()
