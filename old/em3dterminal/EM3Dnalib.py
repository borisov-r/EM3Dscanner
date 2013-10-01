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
# telnetlib for communication
from telnetlib import Telnet


class NetworkAnalyzer:
    """ Main class for communication with PNA.

    Example: pna = NetworkAnalyzer("10.1.15.106", "5024")

    Important ! Use " instead of ' to send IP and Port addresses.
    """
    def __init__(self):
        self.IDN = None             # pna identification
        self.IPaddress = None       # used IP address of pna
        self.Port = None            # used telnet port of pna
        self.Timeout = 5            # time to connect to pna
        self.TimeoutShort = 0.5     # shorter time to wait data from pna
        self.TermChar = "\n"        # termination character
        self.ScpiChar = "SCPI> "    # read_until("SCPI> ")
        # ask pna for system error messages
        self.AskForSystemErrorMsg = "SYSTEM:ERROR?"
        self.tn = None

    def connect(self, IPaddress=None, Port=None):
        self.IPaddress = IPaddress
        self.Port = Port
        # connect to PNA via telnet
        try:
            if self.tn is None and self.IPaddress is not None and self.Port is not None:
                self.tn = Telnet(self.IPaddress, self.Port, self.Timeout)
                self.tn.read_until(self.ScpiChar, self.Timeout)
                self.tn.write("*IDN?")
                self.tn.write(self.TermChar)
                self.IDN = self.tn.read_until(self.TermChar, self.Timeout)
                # flush the pna buffer
                self.tn.read_until(self.ScpiChar, self.Timeout)
                return True
            else:
                print("Already connected to PNA")
                return False
        except:
            print("Error while connecting to PNA")

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

    def setNumberOfMeasurementPoints(self, pointNumber):
        try:
            self.askPna("SENSe1:SWEep:POIN " + str(pointNumber))
        except:
            print("Error when setting measurement points.")

    def getNumberOfMeasurementPoints(self):
        try:
            points = self.askPna("SENSe1:SWEep:POIN?")
            return points
        except:
            print("Error when getting points number from pna.")

    def setFrequencyRange(self, start, stop):
        """ Define start and stop frequencies of the measurement.
         * start - should be given like this: "1ghz"
         * stop  - should be given like this: "2ghz"
        """
        try:
            self.askPna("SENSe1:FREQuency:START " + start)
            self.askPna("SENSe1:FREQuency:STOP " + stop)
        except:
            print("Error while setting frequency range.")

    def getFrequencyRange(self):
        """ Read start and stop frequency from pna.
        returns: string of start / stop frequencies separated by semicolon ";"
        example: >>> pna.askPna("SENS:FREQ:STAR?;STOP?")
                     '+1.00000000000E+010;+1.01000000000E+010'
        """
        try:
            startStop = self.askPna("SENS:FREQ:STAR?;STOP?")
            return startStop
        except:
            print("Error while getting start / stop frequencies from pna.")

    def getPnaIDN(self):
        """ Returns the IDN of PNA like this:
            'Agilent Technologies,N5230C,MY49001380,A.09.42.18'
        """
        try:
            idn = self.askPna("*IDN?")
            return idn
        except:
            print("Error while trying to get PNA's IDN.")

    def getCurrentWorkingDirectory(self):
        try:
            folder = self.askPna("mmem:cdir?")
            return folder
        except:
            print("Error while getting current working directory on pna.")

    def loadDisplaysAndCalibration(self, calibration="calibrationRado.csa"):
        """ Load calibration file on PNA.
        Default file is called: calibrationRado.csa
        """
        try:
            self.askPna("mmem:load 'calibrationRado.csa'")
        except:
            print("Error while trying to load calibration file.")

    def getNamesAndParameters(self):
        """ Get names and paramters of the measurements.
        """
        try:
            parameters = self.askPna("calc:par:cat?")
            return parameters
        except:
            print("Error while getting names and paramters.")

    def setReceiveDataTypeFormat(self, dataType):
        """ Sets data format received from PNA.
         * dataType - can be: "ascii", "real,32" or "real,64"
        """
        try:
            if dataType in ("ascii", "real,32", "real,64"):
                self.askPna("format:data " + dataType)
            else:
                print("Please provide accurate data type formati: 'ascii', 'real,32' or 'real,64'.")
        except:
            print("Error while trying to set data type format.")

    def getReceiveDataTypeFormat(self):
        """ Returns current data type format set for the measurement.
        """
        try:
            format = self.askPna("format:data?")
            return format
        except:
            print("Error while receiveing data type format.")

    def setSparametersFormat(self, parametersType):
        """ Set S-paramters format, while receive data.

        MMEM:STOR:TRAC:FORM:SNP
        MA - Linear Magnitude / degrees
        DB - Log Magnitude / degrees
        RI - Real / Imaginary
        AUTO - data is output in currently selected trace format.
        If other than LogMag, LinMag, or Real/Imag, then output is in Real/Imag.

        Example: self.setSparamtersFormat("MA") # set S-parameters to magnitude.
        """
        try:
            if parametersType in ("MA", "DB", "RI", "AUTO"):
                self.askPna("mmem:stor:trac:form:snp " + parametersType)
            else:
                print("Please provide correct paramters type: 'MA', 'DB', 'RI' or 'AUTO'")
        except:
            print("Error while setting Sparamters format.")

    def setMeasureDataType(self, type):
        """ Select trace to measure.

        Here "type" is trace number that will be measured.
        If trace 2 is set to measure S21 / dB, type is Amplitude, dB.
        If trace 3 is set to measure S21 / Phase, type is Phase, deg.
        After selecting trace received data will be in dB or deg.

        Example: self.setMeasureDataType(3)
                 self.getMeasureData()
                 '+9.36449500000E+001,+1.72543500000E+002' # data in Phase (deg)
                 self.setMeasureDataType(2)
                 self.getMeasureData()
                 '-1.21515400000E+001,-1.21623500000E+001' # data in Amplitude (dB)
        """
        try:
            if str(type) in ("1", "2", "3", "4"):
                self.askPna("calc:par:mnum " + str(type))
            else:
                print("Please select trace number: 1, 2, 3 or 4.")
        except:
            print("Error while setting trace number for the measurement.")

    def getMeasureData(self):
        """ Receive measured data from pna for one point.
        Received data type and format depends from self.setMeasureDataType(type)
        function here and loaded calibration.
        Size of the received data depends from the number of selected sweep points.
        The number of points can be set and get with self.getNumberOfMeasurementPoints()
        and self.setNumberOfMeasurementPoints().
        """
        try:
            data = self.askPna("calc:data? fdata")
            return data
        except:
            print("Error while receiving measured data from pna.")

    def measureSinglePointPhase(self, calibrationFile=None, measureDataType=3):
        """ Measure phase.
        """
        try:
            if calibrationFile is not None:
                self.loadDisplaysAndCalibration(calibrationFile)
            else:
                self.setMeasureDataType(measureDataType)
                return self.getMeasureData()
        except:
            print("Error while measure single point phase.")

    def measureSinglePointAmplitude(self, calibrationFile=None, measureDataType=2):
        """ Measure amplitude.
        """
        try:
            if calibrationFile is not None:
                self.loadDisplaysAndCalibration(calibrationFile)
            else:
                self.setMeasureDataType(measureDataType)
                return self.getMeasureData()
        except:
            print("Error while measure single point phase.")


def main():
    pna = NetworkAnalyzer()
    if pna.connect("10.1.15.106", "5024") is True:
        print("Connected to PNA.")
        # print(pna.IDN)
        pna.askPna("*IDN?")
        print pna.receiveError()
        # print("Load default displays and calibration.")
        pna.askPna("mmem:load 'calibrationRado.csa'")
        # print("Names and parameters of existing measurements for the specified channel:")
        pna.setFrequencyRange("12ghz", "13ghz")
        print pna.getFrequencyRange()
        pna.setNumberOfMeasurementPoints(801)
        print pna.getNumberOfMeasurementPoints()
        print pna.askPna("calc:par:cat?")
        print pna.measureSinglePointAmplitude()
        print pna.measureSinglePointPhase()

    if pna.disconnect() is True:
        print("Disconnected from PNA.")
        print "PNA IDN set to:", pna.IDN


if __name__ == "__main__":
    main()
