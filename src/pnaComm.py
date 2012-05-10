# This file is part of the 3DEMscanner measurement suite.
# 
# 3DEMscanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# 3DEMscanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with 3DEMscanner.  If not, see <http://www.gnu.org/licenses/>.
#
# Purpose of the file: get data from PNA, make it as a structured


from telnetlib import Telnet

class PNA(object):
    """ PNA connection and communication """
    tn = Telnet()               # our main object, should be removed and stay only the object in __init__
    terminationCharacter = "\n" # termination character (executes the command)
    FrequencyPoints = ""        # this is the number of measured frequency points
    answerFromPNA = ""          # data returned from PNA

    def send(self, command):
        try:
            self.tn.write(command.encode(encoding='ascii', errors='strict'))
            self.tn.write(self.terminationCharacter.encode(encoding='ascii', errors='strict'))
            self.tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 5).decode('ascii').strip()
            # last line needed to remove "SCPI> " from the buffer
        except:
            print("Check PNA connection.")
    
    def ask(self, command):
        """ Sends command and returns ascii data  """
        try:
            self.tn.write(command.encode(encoding='ascii', errors='strict'))
            self.tn.write(self.terminationCharacter.encode(encoding='ascii', errors='strict'))
            ans = self.tn.read_until("\n".encode(encoding='ascii', errors='strict'), timeout = 5).decode('ascii').strip()
            self.answerFromPNA = ans
            #print(ans)
            self.tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 5).decode('ascii').strip()
            # last line needed to remove "SCPI> " from the buffer
        except:
            print("Check PNA connection.")
            
    def askBinData(self, command):
        """ Sends command and returns real64 data  """
        try:
            self.tn.write(command.encode(encoding='ascii', errors='strict'))
            self.tn.write(self.terminationCharacter.encode(encoding='ascii', errors='strict'))
            ans = self.tn.read_until("\n".encode(encoding='ascii', errors='strict'), timeout = 5)
            self.answerFromPNA = ans
            print(ans)
            self.tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 5).decode('ascii').strip()
            # last line needed to remove "SCPI> " from the buffer
        except:
            print("Check PNA connection.")
        
    def __init__(self, host, port):
        """ Connection to PNA """    
        try:
            self.tn = Telnet(host, port, timeout=10)    #
            ans = self.tn.read_until("SCPI> ".encode(encoding='ascii', errors='strict'), timeout = 10).decode('ascii').strip()
            print(ans)
            self.ask("*IDN?")
        except:
            print("Error while connecting.")
    
    def closeConnectionToPNA(self):
        self.tn.close()
        print("Connection to PNA closed")
    
    def checkSystemError(self):
        self.ask("system:error?")
    
    def resetPNAdisplay(self):
        self.send("syst:fpr")
        print("Display reset.")
    
    def loadCalibration(self, fileName):
        message = "mmem:load " + "\'" + fileName + "\'"
        self.send(message)
        print("Calibration loaded.")
                
    def checkDataFormat(self):
        self.ask("format:data?")
    
    def setDataFormat(self, command):
        """ Command should be: "real32", "real64" or "ascii" """
        if( command == "real32" ):
            self.send("format:data real,32")
        elif( command == "real64" ):
            self.send("format:data real,64")
        elif( command == "ascii" ):
            self.send("format:data ascii") 

    def selectTraceNum(self, command):
        """ Select one of the traces on PNA: "1", "2", "3" ... """
        self.send("calc:par:mnum " + command)
        
    def catalogMeasurements(self):
        self.ask("CALC:PAR:CAT:EXT?")
    
    def getReal32SNP(self, command):
        """ Sets data:format to real32 and gets selected SNP """
        self.setDataFormat("real32")
        self.askBinData("calc:data:snp:ports? " + "\"" + command + "\"")
        
    def getReal64SNP(self, command):
        """ Sets data:format to real64 and gets selected SNP """
        self.setDataFormat("real64")
        self.askBinData("calc:data:snp:ports? " + "\"" + command + "\"")    
        
    def getAsciiSNP(self, command):
        """ Sets data:format to real64 and gets selected SNP """
        self.setDataFormat("ascii")
        self.ask("calc:data:snp:ports? " + "\"" + command + "\"")
        
    def getSNPformat(self):
        self.ask("mmem:stor:trace:format:snp?")
        
    def setSNPformat(self, command):
        """ MMEM:STOR:TRAC:FORM:SNP 
        MA - Linear Magnitude / degrees
        DB - Log Magnitude / degrees
        RI - Real / Imaginary
        AUTO - data is output in currently selected trace format. 
        If other than LogMag, LinMag, or Real/Imag, then output is in Real/Imag.
        """
        if( command == "ma" ):
            self.send("mmem:stor:trac:form:snp MA")
        elif( command == "dB" ):
            self.send("mmem:stor:trac:form:snp DB")
        elif( command == "ri" ):
            self.send("mmem:stor:trac:form:snp RI") 
        elif( command == "auto" ):
            self.send("mmem:stor:trac:form:snp AUTO")
        else:
            print("Please provide correct data")
            
            
    def getPNASweepPoints(self):
        self.ask("sens:swe:poin?")
        self.FrequencyPoints = self.answerFromPNA
        
    def setPNASweepPoints(self, points):
        self.send("sens:swe:poin " + points)