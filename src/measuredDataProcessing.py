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
import numpy as np

#class PlaneXYGrid:
#            
#    def __init__(self, xAxisPoints, yAxisPoints, zAxisPoints, frequency):
#        print("Data array defined")
#        self.Xpoints = xAxisPoints
#        self.Ypoints = yAxisPoints
#        self.FrequencyNumber = frequency    # this is the PNA sweep frequency number "FrequencyPoints"
#        self.amplitudeData = np.zeros((self.Xpoints,self.Ypoints), dtype=np.float64)
#        self.phaseData = np.zeros((self.Xpoints,self.Ypoints), dtype=np.float64)
#        
#    def printAmp(self):
#        print(self.amplitudeData)
#    
#    def printPhase(self):
#        print(self.phaseData)
#    
#    def setCurrentPointAmplitude(self, xPoint, yPoint, amplitude):
#        self.amplitudeData[xPoint,yPoint] = amplitude
#        
#    def setCurrentPointPhase(self, xPoint, yPoint, phase):
#        self.phaseData[xPoint,yPoint] = phase
#        
#    def getCurrentPointAmplitude(self, xPoint, yPoint):
#        print(self.amplitudeData[xPoint, yPoint])
#    
#    def getCurrentPointPhase(self, xPoint, yPoint):
#        print(self.phaseData[xPoint, yPoint])   
#    
#    def writePlaneToFiles(self, fileName):
#        # two files are generated from one plane in 2 directories "amplitude" and "phase"
#        np.save(fileName + "amp.npy", self.amplitudeData)
#        np.save(fileName + "ph.npy", self.phaseData)
#        
#    def readPlaneFromFile(self, fileName):
#        if "amp.npy" in fileName: 
#            self.amplitudeData = np.load(fileName)
#        elif "ph.npy" in fileName:
#            self.phaseData = np.load(fileName)
#        else:
#            print("Please provide correct file name.")
#
#class CubeXYGrid(object):
#    #test
#    def __init__(self):
#        self.cubeArray = []

class SinglePointDataProcessing(object):
    # description:
    #    handle data measured from PNA for single point: array of freq, amp, phase
    def __init__(self, stringArrayFromPNA, freqPoints):
        self.data = stringArrayFromPNA
        self.data = self.data.split(',')
        self.FrequencyRange = self.data[0:int(freqPoints)]
        self.AmplitudeData = self.data[int(freqPoints):2*int(freqPoints)]
        self.PhaseData = self.data[2*int(freqPoints):]
        

    def toFloat(self, stringList):
        for index in range(len(stringList)):
            stringList[index] = float(stringList[index])
        return stringList
    
    def getFrequencyData(self):
        self.floatFrequencyRange = self.toFloat(self.FrequencyRange)    # list of amplitudes as float list
        #print(self.floatFrequencyRange) # debug function
        return self.floatFrequencyRange
        
    def getAmplitudeData(self):
        self.floatAmplitude = self.toFloat(self.AmplitudeData)    # list of amplitudes as float list
        #print(self.floatAmplitude) # debug function
        return self.floatAmplitude
        
    def getPhaseData(self):
        self.floatPhase = self.toFloat(self.PhaseData)
        #print(self.floatPhase) # debug function
        return self.PhaseData

class PlaneXYGrid(object):
    # description:
    #   handles data points of xy plane for one frequency
    def __init__(self, xMax, yMax):
        print("Data array defined") # debug purposes
        self.Xpoints = xMax
        self.Ypoints = yMax
        self.Data = np.zeros((self.Xpoints,self.Ypoints), dtype=np.float64)
        
    def addPointData(self, xCoord, yCoord, pointData):
        try:
            self.Data[xCoord,yCoord] = pointData
        except:
            print("Please provide correct pointData.")
        
        
        
        
        
         