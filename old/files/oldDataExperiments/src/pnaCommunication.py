from telnetlib import Telnet
from struct import *
import numpy as np

class PNA(object):
    """ PNA connection and communication """
    tn = Telnet()               # our main object, should be removed and stay only the object in __init__
    terminationCharacter = "\n" # termination character (executes the command)
    FrequencyPoints = ""
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
            
    def getPNASweepPoints(self):
        self.ask("sens:swe:poin?")
        self.FrequencyPoints = self.answerFromPNA
        
    def setPNASweepPoints(self, points):
        self.send("sens:swe:poin " + points)

class PlaneXYGrid:
            
    def __init__(self, xAxisPoints, yAxisPoints, zAxisPoints, frequency):
        print("Data array defined")
        self.Xpoints = xAxisPoints
        self.Ypoints = yAxisPoints
        self.FrequencyNumber = frequency    # this is the PNA sweep frequency number "FrequencyPoints"
        self.amplitudeData = np.zeros((self.Xpoints,self.Ypoints), dtype=np.float64)
        self.phaseData = np.zeros((self.Xpoints,self.Ypoints), dtype=np.float64)
        
    def printAmp(self):
        print(self.amplitudeData)
    
    def printPhase(self):
        print(self.phaseData)
    
    def setCurrentPointAmplitude(self, xPoint, yPoint, amplitude):
        self.amplitudeData[xPoint,yPoint] = amplitude
        
    def setCurrentPointPhase(self, xPoint, yPoint, phase):
        self.phaseData[xPoint,yPoint] = phase
        
    def getCurrentPointAmplitude(self, xPoint, yPoint):
        print(self.amplitudeData[xPoint, yPoint])
    
    def getCurrentPointPhase(self, xPoint, yPoint):
        print(self.phaseData[xPoint, yPoint])   
    
    def writePlaneToFiles(self, fileName):
        # two files are generated from one plane in 2 directories "amplitude" and "phase"
        np.save(fileName + "amp.npy", self.amplitudeData)
        np.save(fileName + "ph.npy", self.phaseData)
        
    def readPlaneFromFile(self, fileName):
        if "amp.npy" in fileName: 
            self.amplitudeData = np.load(fileName)
        elif "ph.npy" in fileName:
            self.phaseData = np.load(fileName)
        else:
            print("Please provide correct file name.")
 
class CubeXYGrid(object):
    #test
    def __init__(self):
        self.cubeArray = []

class SinglePointDataProcessing(object):
    # description
    def __init__(self, stringArrayFromPNA, freqPoints):
        self.data = stringArrayFromPNA
        self.FrequencyRange = self.data.strip(",")[0:freqPoints]
        self.AmplitudeData = self.data[freqPoints:2*freqPoints]
        #self.PhaseData = self.data[2*freqPoints:]

    def toFloat(self, stringList):
        for index in range(len(stringList)):
            stringList[index] = float(stringList[index])
        return stringList
    
    def getAmplitudeData(self):
        self.floatAmplitude = self.toFloat(self.AmplitudeData)    # list of amplitudes as float list
        print(self.floatAmplitude)
        
    #def getPhaseData(self):
        #self.floatPhase = self.toFloat(self.PhaseData)
        

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
a.getPNASweepPoints()

b = SinglePointDataProcessing(snp,int(a.FrequencyPoints))
b.getAmplitudeData()

a.checkSystemError()
a.closeConnectionToPNA()
    