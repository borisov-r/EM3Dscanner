from serial import Serial
from time import sleep


class RepRap(object):
    """ Communication with reprap.
    """
    def __init__(self):
        self.term = "\r\n"
        self.port = None
        self.baudrate = None
        self.printer = None
        self.xPoints = None
        self.yPoints = None
        self.zPoints = None

    def connect(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        try:
            self.printer = Serial(self.port, self.baudrate)
            # add these to log file
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            self.printer.readline().strip()
            # set to work with relative coordinates !
            self.printer.write("G91" + self.term)
        except:
            print "Error while connecting to printer."

    def setX(self, numXpoints):
        self.x = numXpoints

    def setY(self, numYpoints):
        self.y = numYpoints

    def setZ(self, numZpoints):
        self.z = numZpoints

    def disconnect(self):
        if self.printer is not None:
            try:
                self.printer.close()
            except:
                print "Error while disconnecting."
        else:
            print "Already disconnected."

    def move(self, ff=True, moveX=0, moveY=0, moveZ=0, speed=100, wait=True):
        """ Move reprap with default speed 100 mm/min.
        ff is parameter that defines the movement direction.
            True - forward (+ direction)
            False - backwards (- direction)
        """
        if ff:
            sign = "+"
        else:
            sign = "-"
        if self.printer is not None:
            self.printer.write("G91" + self.term)
            self.printer.readline().strip()
            word = "G1 X" + sign + str(moveX) + " Y" + sign + str(moveY) + " Z" + sign + str(moveZ) + " F" + str(speed)
            self.printer.write(word + self.term)
            # should go in log file !
            #print self.printer.readline().strip()
            sleep(0.5)
            if wait:
                word = "M400" + self.term
                self.printer.write(word)
                # should go in log file !
                self.printer.readline().strip()
        else:
            print "Check printer connection."

    def moveOneSlice(self):
        """ Move one slice X and Y.
        """
        for i in range(self.y):
            # check
            for j in range(self.x):
                if i & 1:
                    self.move(False, 1)
                else:
                    self.move(True, 1)
                print "X is: ", j
                print "Y is: ", i
            # if not end point move
            if i != (self.y - 1):       # stay at the end point
                self.move(True, 0, 1)

z = 5
y = 5
x = 5
p = RepRap()
p.connect("/dev/ttyACM0", 115200)
p.setX(x)
p.setY(y)
p.setZ(z)
p.moveOneSlice()
#p.move(10)
#for i in range(y):
    # check
#    for j in range(x):
#        if i & 1:
#            p.move(True, 1)
#        else:
#            p.move(False, 1)
#        print "X is: ", j
#        print "Y is: ", i
#    p.move(True, 0, 1)
p.disconnect()
