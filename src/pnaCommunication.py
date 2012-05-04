from telnetlib import Telnet
from struct import *

class PNA(object):
    """ PNA connection and communication """
    tn = Telnet()   # out main object
    terminationCharacter = "\n" # termination character (executes the command)
    answerFromPNA = ""

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
            print(ans)
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
            self.tn = Telnet(host, port, timeout=10)
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
    
a = PNA("10.1.15.106", "5024")
#.write("*IDN?".encode(encoding='ascii', errors='strict'))
a.resetPNAdisplay()
a.loadCalibration("calibrationRado.csa")
a.checkDataFormat()
a.checkSystemError()
#a.setDataFormat("real32")
#a.checkDataFormat()
#a.checkSystemError()
#a.setDataFormat("real64")
#a.checkDataFormat()
#a.checkSystemError()
#a.setDataFormat("ascii")
#a.checkDataFormat()
#a.checkSystemError()
a.catalogMeasurements()
a.selectTraceNum("1")
a.getAsciiSNP("2")
snp = a.answerFromPNA
print(snp)
pp = float(snp[0:19])
ppp = float(snp[21:39])
pppp = float(snp[40:59])
print(pp)
print(ppp)
print(pppp)
print(pack('d', pp))
f=open('my-file.bin', 'wb')
f.write(pack('d', pp))
f.close()
f=open('my-file.bin', 'r+b')
print(f.tell())
print(f.seek(8))
f.write(pack('d', ppp))
f.close()
f=open('my-file.bin', 'r+b')
print(f.seek(16))
f.write(pack('d', pppp))
f.close()

f=open('my-file.bin', 'r+b')
one = [0] * 3
one[0] = unpack('d', f.read(8))
one[1] = unpack('d', f.read(8))
one[2] = unpack('d', f.read(8))
f.close()

print(len(one))
print(one[0])
print(one[1])
print(one[2])

a.checkSystemError()
a.closeConnectionToPNA()
    