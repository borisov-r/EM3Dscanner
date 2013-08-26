from LogFile import logging
from LogFile import LogData
from EM3Dreprap import RepRap


class Scanner(object):
    ''' Implementation of the scan algorithm
    '''
    def __init__(self, logging, rr, of, mp, step):
        ''' Initialize Scanner object:
                logging - make log in file
                rr      - reprap object
                of      - output file object
                mp      - measurement points is Tuple with 3 elements
                          (xPoints, yPoints, zPoints)
                step    - step size 0.1 to 100 mm. Tuple (XY, Z)

                Volume will be for example: 20 x 10 x 5 = 1000 points

        '''
        self.log = logging
        self.rr = rr  # RepRap object available for all methods
        self.of = of  # output file object
        self.points = mp  # measurement points (tuple)
        self.stepXY = step[0]
        self.stepZ = step[1]
        pass

    def oneRow(self):
        # move one row
        if self.rr.connected:
            print self.rr.getCurrentCoordinates()
            x = self.createStepPointsX()
            for i in range(len(x)):
                print x[i]
            for i in range(len(x)):
                print x[len(x) - i - 1]
        pass

    def getCoordTuple(self):
        # takes current coordinates and return tuple of floats
        if self.rr.connected:
            currentCoords = self.rr.getCurrentCoordinates()
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
        print self.points[0]
        print type(self.points)
        for x in range(self.points[0]):
            pnts.append(round((currPoint + self.stepXY), 3))
            # current point is set to x-th element
            currPoint = pnts[x] + self.stepXY
            self.log.append("current point x set to: %s" % currPoint)
        lastElement = pnts.pop()    # remove last element from the list
        self.log.append("last element x axis removed: %s" % lastElement)
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
        lastElement = pnts.pop()    # remove last element from the list
        self.log.append("last element y axis removed: %s" % lastElement)
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
        lastElement = pnts.pop()    # remove last element from the list
        self.log.append("last element z axis removed: %s" % lastElement)
        self.log.append("points z axis at the end: %s" % pnts)
        #
        # if everything is correct return list with the coordinates
        return pnts

    def moveOneStepX(self, coords):
        if self.rr.connected:
            currentCoordinates = self.getCoordTuple()
            print currentCoordinates
            print type(currentCoordinates)
            self.log.append("Current coordinates: x(%s) y(%s) z(%s)"
                            % currentCoordinates)
            #
            #if currentCoordinates[0] in coords:
            #    place = coords.index(currentCoordinates[0])
            #    print place
            if 1.5 in coords:
                # return position of the element with value
                place = coords.index(1.5)
                self.log.append("Current element position in list: %s"
                                % place)
                print place


def main():
    log = LogData(logging.INFO)
    rr = RepRap()
    rr.connect(port="/dev/ttyACM0", baudrate=115200)
    scan = Scanner(log, rr, "em3d.out", (13, 10, 5), (0.5, 0.1))
    scan.oneRow()
    scan.getCoordTuple()
    x = scan.createStepPointsX()
    y = scan.createStepPointsY()
    z = scan.createStepPointsZ()
    print x
    print y
    print z
    scan.oneRow()
    scan.moveOneStepX(x)
    pass

if __name__ == '__main__':
    main()
