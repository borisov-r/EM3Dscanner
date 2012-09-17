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
# Purpose of the file: main tests and experiments with main classes


from pnaComm import PNA
from measuredDataProcessing import SinglePointDataProcessing, PlaneXYGrid
from reprapComm import RepRap

r = RepRap(115200)
word = r.move("X", "+", "10", "300")
r.write(word.encode("ascii"))
r.disconnect()

a = PNA("10.1.15.106", "5024")
a.resetPNAdisplay()
a.loadCalibration("calibrationRado.csa")
a.checkDataFormat()
a.checkSystemError()

a.getPNASweepPoints() # ! don't forget to take frequency number !
print(a.FrequencyPoints)
print(a.getNumberOfFrequencyPoints())

a.selectTraceNum("2") # very important ! don't forget to select trace
a.getAsciiSNP("2")
snp = a.answerFromPNA

b = SinglePointDataProcessing(snp, a.FrequencyPoints)
print("Frequencies")
print(b.getFrequencyData())
print("Amplitudes")
print(b.getAmplitudeData())
print("Phases")
print(b.getPhaseData())

c = PlaneXYGrid(10, 10)
c.addPointData(3, 3, b.floatAmplitude[3])
print("Array data is: ")
print(c.Data[3,3])

a.checkSystemError()
a.closeConnectionToPNA()