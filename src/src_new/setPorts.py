"""
This class should:
    1. list all /dev/ttyUSB* and /dev/ttyACM* ports
    2. ask for correct arrangement of RX and TX
    3. should return plain text with RX and TX ports in plain text
"""

from os import listdir


class SetDevices(object):
    """
    Sets RX and TX usb port to correct devices
    """
    def __init__(self):
        self.receiver = None
        self.transmitter = None
        self.reprap = None

    def listDevTTY(self, folder):
        """
        When the class is initialized this function should fill
        the variables with tuples for every port.
            ttyUSB0 should be connected to RECEIVER
            ttyUSB1 should be connected to TRANSMITTER
            ttyACM0 should be connected to RepRap
        """
        self.p = listdir(folder)
        if 'ttyUSB0' in self.p:
            self.receiver = ('/dev/ttyUSB0')
        if 'ttyUSB1' in self.p:
            self.transmitter = ('/dev/ttyUSB1')
        if 'ttyACM0' in self.p:
            self.reprap = ('/dev/ttyACM0')

    def printPorts(self):
        """
        This function is used to print found ports in the terminal only.
        """
        if self.receiver is not None:
            print self.receiver
        if self.transmitter is not None:
            print self.transmitter
        if self.reprap is not None:
            print self.reprap


def main():
    # here should be the main code
    test = SetDevices()
    test.listDevTTY('/dev')
    test.printPorts()
    pass

if __name__ == "__main__":
    main()
