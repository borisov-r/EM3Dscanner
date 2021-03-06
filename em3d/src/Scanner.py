import sys
from LogFile import logging
from LogFile import LogData
from EM3Dreprap import RepRap


class Scanner(object):
    ''' Implementation of the scan algorithm
    '''
    def __init__(self, logging, rr, na, of, mp, step):
        ''' Initialize Scanner object:
                logging - make log in file
                rr      - reprap object
                na      - network analyzer
                of      - output file object
                mp      - measurement points is Tuple with 3 elements
                          (xPoints, yPoints, zPoints)
                step    - step size 0.1 to 100 mm. Tuple (XY, Z)

                Volume will be for example: 20 x 10 x 5 = 1000 points

        '''
        self.log = logging
        self.rr = rr  # RepRap object available for all methods
        self.na = na  # network analyzer object
        self.of = of  # output file object
        self.points = mp  # measurement points (tuple)
        self.stepXY = step[0]
        self.stepZ = step[1]
        self.percent = 0

    def getCoordTuple(self):
        # takes current coordinates and return tuple of floats
        if self.rr.connected:
            currentCoords = self.rr.getCurrentCoordinates()
            self.log.append("currentCoords(%s)" % currentCoords)
            x = currentCoords.translate(None, "XYZE")
            y = x[1:]  # remove first ":"
            z = y[0:len(y) - 5]  # remove extruder coordinates
            coords = z.split(":")
            self.log.append("coords: %s" % coords)
            coordsTuple = (float(coords[0]),
                           float(coords[1]),
                           float(coords[2]))
            self.log.append("coordsT: x(%s) y(%s) z(%s)" % coordsTuple)
            #print coordsTuple
            #print self.points
            return coordsTuple

    def createStepPointsX(self):
        # create step points in the for X axis
        pp = self.getCoordTuple()
        pnts = [float(pp[0])]  # create empty list
        self.log.append("points: %s" % pnts)
        currPoint = pnts[0]
        #print self.points[0]
        #print type(self.points)
        for x in range(self.points[0]):
            pnts.append(round((currPoint + self.stepXY), 3))
            # current point is set to x-th element
            currPoint = pnts[x] + self.stepXY
            self.log.append("current point x set to: %s" % currPoint)
        #lastElement = pnts.pop()    # remove last element from the list
        #self.log.append("last element x axis removed: %s" % lastElement)
        self.log.append("points x axis at the end: %s" % pnts)
        #
        # if everything is correct return list with the coordinates
        return pnts

    def createStepPointsY(self):
        # create step points in the for X axis
        pp = self.getCoordTuple()
        pnts = [float(pp[1])]  # create empty list
        self.log.append("points: %s" % pnts)
        currPoint = pnts[0]
        for y in range(self.points[1]):
            pnts.append(round((currPoint + self.stepXY), 3))
            # current point is set to x-th element
            currPoint = pnts[y] + self.stepXY
            self.log.append("current point y set to: %s" % currPoint)
        #lastElement = pnts.pop()    # remove last element from the list
        #self.log.append("last element y axis removed: %s" % lastElement)
        self.log.append("points y axis at the end: %s" % pnts)
        #
        # if everything is correct return list with the coordinates
        return pnts

    def createStepPointsZ(self):
        # create step points in the for X axis
        pp = self.getCoordTuple()
        pnts = [float(pp[2])]  # create empty list
        self.log.append("points: %s" % pnts)
        currPoint = pnts[0]
        for z in range(self.points[2]):
            pnts.append(round((currPoint + self.stepZ), 3))
            # current point is set to x-th element
            currPoint = pnts[z] + self.stepZ
            self.log.append("current point z set to: %s" % currPoint)
        #lastElement = pnts.pop()    # remove last element from the list
        #self.log.append("last element z axis removed: %s" % lastElement)
        self.log.append("points z axis at the end: %s" % pnts)
        #
        # if everything is correct return list with the coordinates
        return pnts

    def trunc(self, f, n):
        '''Truncates/pads a float f to n decimal places without rounding'''
        return ('%.*f' % (n + 1, f))[:-1]

    def mX(self):
        ''' Move x axis
            pl      - point list
            na      - network analyzer to get parameters
            of      - output file
            currY   - current Y coordinate
        '''
        px = self.createStepPointsX()  # list of point on x axis
        #self.rr.printer.write("G90\n")
        #print self.rr.printer.readline().strip()
        self.log.append("mX entered with G90 command - absolute coordinates")
        for i in range(len(px)):
            self.log.append("x i(%s) px(%s)" % (i, px[i]))
            if i == 0:
                # if first point is 0, then we have to read only once
                self.rr.printer.write("G1 X" + str(px[i]) + "\n")
                self.log.append("(G1 X" + str(px[i]) + ") written to printer")
                i1 = self.rr.printer.readline().strip()
                i2 = None
                sys.stdout.flush()
            elif i > 0:
                # if more points wait for Movement finished and send next
                self.rr.printer.write("G1 X" + str(px[i]) + "\n")
                self.log.append("(G1 X" + str(px[i]) + ") written to printer")
                i1 = self.rr.printer.readline().strip()
                while 1:
                    i2 = self.rr.printer.readline().strip()
                    if 'Movement' in i2:
                        #self.log.warn(".")
                        sys.stdout.flush()
                        self.log.append("i(%s) Movement finished." % i)
                        break
                    else:
                        pass
            else:
                # else pass everything
                i1 = None
                i2 = None
                pass
            #
            #print i1, i2
            self.log.append("i1(%s) i2(%s)" % (i1, i2))
            currPosition = self.rr.getCurrentCoordinates()
            #print currPosition
            data = "+2.80000000000E+010,+2.80100000000E+010"
            self.of.appendToFile(currPosition, data)
            #print px[i]
            percent = (i / float(len(px)) * 100.0)
            #self.log.append("Current percent: %s" % percent)
            self.percent = self.trunc(percent, 1)
            #self.log.append("Current percent self: %s" % self.percent)
            if i == len(px) - 1:
                print ('\rX axis: 100.0 %'),
            else:
                print ('\rX axis: %s' % self.percent),
                print ('%'),
        #
        self.percent = "100.0"
        print("\nPercents done: " + self.percent + "%")
        self.rr.printer.write("G1 X" + str(px[0]) + "F3000\n")
        self.rr.printer.write(self.rr.printer.readline().strip())
        self.rr.printer.write(self.rr.printer.readline().strip())
        #del px
        return True

    def mY(self):
        ''' Move Y axis
            pl      - point list
            na      - network analyzer to get parameters
            of      - output file
            currY   - current Y coordinate
        '''
        py = self.createStepPointsY()  # list of point on x axis
        #
        for i in range(len(py)):
            if i == 0:
                self.rr.printer.write("G1 Y" + str(py[i]) + "\n")
                self.log.append("(G1 Y" + str(py[i]) + ") written to printer")
                # wait till receive Movement finished
                '''
                while 1:
                    i2 = self.rr.printer.readline().strip()
                    if 'Movement' in i2:
                        #self.log.warn(".")
                        sys.stdout.flush()
                        self.log.append("i(%s) Movement finished." % i)
                        break
                    else:
                        pass
                '''
                # start X measurement
                while 1:
                    if self.mX():
                        self.log.append("y i(%s) py(%s)" % (i, py[i]))
                        break
                    else:
                        pass
            elif i > 0:
                self.rr.printer.write("G1 Y" + str(py[i]) + "\n")
                self.log.append("(G1 Y" + str(py[i]) + ") written to printer")
                # wait till receive Movement finished
                while 1:
                    i2 = self.rr.printer.readline().strip()
                    if 'Movement' in i2:
                        #self.log.warn(".")
                        sys.stdout.flush()
                        self.log.append("i(%s) Movement finished." % i)
                        self.log.append("i2(%s) Movement finished." % i2)
                        break
                    else:
                        pass
                # start X measurement
                while 1:
                    if self.mX():
                        self.log.append("y i(%s) py(%s)" % (i, py[i]))
                        break
                    else:
                        pass
        return True

    def mm(self):
        ''' Create coordinates and move all cube.
        '''
        x = self.createStepPointsX()
        y = self.createStepPointsY()
        z = self.createStepPointsZ()
        #
        messageX = "G1 X" + str(x[0])
        messageY = " Y" + str(y[0])
        messageZ = " Z" + str(z[0])
        #
        message = messageX + messageY + messageZ
        #
        self.log.append("Message (%s)" % message)
        print message
        #
        i = 0  # x counter
        j = 0  # y counter
        k = 0  # z counter
        #
        while 1:
            #
            # start with the first point
            #if x[i] == 0 and j == 0 and k == 0:
            #    messageX = "G1 X" + str(x[i])
            #    message = messageX + messageY + messageZ
            #    i = i + 1
                #print(message)
            #
            # move x while less than
            if j > 0 and j < len(y):

                if i > 0 and i < len(x):
                    messageX = "G1 X" + str(x[i])
                    message = messageX + messageY + messageZ
                    print(message)
                i = i + 1
            j = j + 1
            i = 0
            #print j
            '''
            else:
                print("X[i] = %s" % (x[i])),
                print("Y[j] = %s" % (y[j])),
                print("Z[k] = %s" % (z[k])),
                print("i, %s" % i),
                print("j, %s" % j),
                print("k, %s" % j)
            '''


def main():
    log = LogData(logging.INFO)
    rr = RepRap()
    rr.connect(port="/dev/ttyACM0", baudrate=115200)
    scan = Scanner(log, rr, "em3d.out", (13, 10, 5), (0.5, 0.1))
    scan.getCoordTuple()
    #x = scan.createStepPointsX()
    #y = scan.createStepPointsY()
    #z = scan.createStepPointsZ()
    #print x
    #print y
    #print z
    #scan.oneRow()
    #scan.moveOneStepXforward("1.5", '-')
    list = [0.0, 1.0, 2.0, 30.0, 4.0, 5.0, 100.0, 7.0, 8.0, 9.0, 10.0, 16.0]
    scan.mX(list, "na", "of")
    rr.disconnect()
    pass

if __name__ == '__main__':
    main()
