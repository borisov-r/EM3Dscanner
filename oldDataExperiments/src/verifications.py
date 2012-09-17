# No1
#---------------------------------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------------------------------

#No2
#---------------------------------------------------------------------------------------------------------------------
grid1 = PlaneXYGrid(2,2,2,1)
grid1.setCurrentPointAmplitude(1, 1, -2.5)
grid1.setCurrentPointAmplitude(0, 0, 2.5)
grid1.printAmp()
grid1.printPhase()
#print("Number of sweep points: ")
a.getPNASweepPoints()
a.setPNASweepPoints("101")
print("test")
print(a.frequencyPoints)
a.getPNASweepPoints()
print(a.frequencyPoints)
print(a.getAsciiSNP("2"))
#---------------------------------------------------------------------------------------------------------------------

#No3
#---------------------------------------------------------------------------------------------------------------------
a.selectTraceNum("1")
a.getAsciiSNP("2")
snp = a.answerFromPNA

data = list()
list(snp)
print(len(snp))
data = snp.split(",")

for index in range(len(data)):
    data[index] = float(data[index])
    
print(data)

grid1 = PlaneXYGrid(2,2,2,a.FrequencyPoints)
grid1.setCurrentPointAmplitude(0, 0, data[2])
grid1.setCurrentPointAmplitude(1, 1, data[3])
grid1.setCurrentPointPhase(0, 0, data[4])
grid1.setCurrentPointPhase(1, 1, data[5])
grid1.printAmp()
grid1.printPhase()

grid1.writePlaneToFiles("meas090512")

grid1 = PlaneXYGrid(2,2,2,a.FrequencyPoints)
grid1.setCurrentPointAmplitude(0, 0, 0.0)
grid1.setCurrentPointAmplitude(1, 1, 0.0)
grid1.setCurrentPointPhase(0, 0, 0.0)
grid1.setCurrentPointPhase(1, 1, 0.0)

grid1.printAmp()
grid1.printPhase()

grid1.readPlaneFromFile("meas090512amp.npy")
grid1.readPlaneFromFile("meas090512ph.npy")
grid1.printAmp()
grid1.printPhase()
#---------------------------------------------------------------------------------------------------------------------

#No4
#---------------------------------------------------------------------------------------------------------------------
data = list()
list(snp)

a.getPNASweepPoints()

print(len(snp))
data = snp.split(",")
print("Data float elements are: ")
print(len(data))

temp = int( len(data) / 3 )
print("temp is")
print(temp)

# taka only amplitude and phase without frequencies
data = data[temp:]

print(data)

#for index in range(len(data)):
#    data[index] = float(data[index])
data = toFloat(data)

print("Float data is: ")    
print(data)

a.getPNASweepPoints()

grid1 = PlaneXYGrid(len(data)/3,len(data)/3,2,int(a.FrequencyPoints))
grid1.setCurrentPointAmplitude(0, 0, data[2])
grid1.setCurrentPointAmplitude(1, 1, data[3])
grid1.setCurrentPointPhase(0, 0, data[4])
grid1.setCurrentPointPhase(1, 1, data[5])
grid1.printAmp()
grid1.printPhase()

grid1.writePlaneToFiles("meas090512")

grid1 = PlaneXYGrid(2,2,2,a.FrequencyPoints)
grid1.setCurrentPointAmplitude(0, 0, 0.0)
grid1.setCurrentPointAmplitude(1, 1, 0.0)
grid1.setCurrentPointPhase(0, 0, 0.0)
grid1.setCurrentPointPhase(1, 1, 0.0)

grid1.printAmp()
grid1.printPhase()

grid1.readPlaneFromFile("meas090512amp.npy")
grid1.readPlaneFromFile("meas090512ph.npy")
grid1.printAmp()
grid1.printPhase()

b = CubeXYGrid()
b.cubeArray.append(grid1.amplitudeData)
b.cubeArray.append(grid1.phaseData)

print("Print cube data: ")

print(b.cubeArray[0])
print(b.cubeArray[1])

#No5
#---------------------------------------------------------------------------------------------------------------------