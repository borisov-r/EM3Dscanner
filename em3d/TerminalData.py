import logging
from LogFile import LogData


class TerminalData(object):
    ''' Get data from terminal for X, Y and Z points, resolution and more"
    '''
    def __init__(self, logging):
        ''' Generate object with obption for logging to file.
            Pass LogData object as logging parameter.
        '''
        self.log = logging
        self.log.append("### TerminalData log started")
        self.rawInputValue = None  # temporary store value
        self.MIN_XY_AXIS = 0
        self.MAX_XY_AXIS = 2000
        self.MIN_Z_AXIS = 0
        self.MAX_Z_AXIS = 1200
        pass

    def printMessage(self, message):
        ''' Print question to terminal
        '''
        print(message),
        self.log.append("Console message (%s)" % message)
        return True

    def getIntegerInput(self, message, min, max):
        ''' Show message to console and get input in range (min, max).
            After input the value is stored in temporary variable:
                self.rawInputValue
            the value should be stored in immutable variable so that
            the number of points don't change during measurement.
        '''
        while True:
            #
            value = int(raw_input(message))
            self.log.append("Raw integer input (%s)" % value)
            #
            if value > min and value < max:
                self.rawInputValue = value
                self.log.append("Input from console set to (%s)" % value)
                break
            elif value == min:
                self.rawInputValue = value
                self.log.append("Input from console set to (%s)" % value)
                break
            elif value == max:
                self.rawInputValue = value
                self.log.append("Input from console set to (%s)" % value)
                break
            else:
                self.log.append("Input Error min(%s) max(%s) value(%s)"
                                % (min, max, value))

    def getFloatInput(self, message, min, max):
        ''' Show message to console and get input in range (min, max).
            After input the value is stored in temporary variable:
                self.rawInputValue
            the value should be stored in immutable variable so that
            the number of points don't change during measurement.
        '''
        while True:
            #
            value = float(raw_input(message))
            self.log.append("Raw float input (%s)" % value)
            #
            if value > min and value < max:
                self.rawInputValue = value
                self.log.append("Input from console set to (%s)" % value)
                break
            elif value == min:
                self.rawInputValue = value
                self.log.append("Input from console set to (%s)" % value)
                break
            elif value == max:
                self.rawInputValue = value
                self.log.append("Input from console set to (%s)" % value)
                break
            else:
                self.log.append("Input Error min(%s) max(%s) value(%s)"
                                % (min, max, value))

    def getXYZpoints(self):
        ''' Ask for number of points for all axis and return Tuple
        '''
        self.log.append("### Collect XYZ measurement points number")
        # get X axis points
        message = ("Number of points on X axis (%s - %s): "
                   % (self.MIN_XY_AXIS, self.MAX_XY_AXIS))
        self.getIntegerInput(message,
                             self.MIN_XY_AXIS,
                             self.MAX_XY_AXIS)
        xPoints = (self.rawInputValue)
        #
        # get Y axis points
        message = ("Number of points on Y axis (%s - %s): "
                   % (self.MIN_XY_AXIS, self.MAX_XY_AXIS))
        self.getIntegerInput(message,
                             self.MIN_XY_AXIS,
                             self.MAX_XY_AXIS)
        yPoints = (self.rawInputValue)
        #
        # get Z axis points
        message = ("Number of points on Z axis (%s - %s): "
                   % (self.MIN_Z_AXIS, self.MAX_Z_AXIS))
        self.getIntegerInput(message,
                             self.MIN_Z_AXIS,
                             self.MAX_Z_AXIS)
        zPoints = (self.rawInputValue)
        #
        self.log.append("xPoints(%s), yPoints(%s), zPoints(%s)"
                        % (xPoints, yPoints, zPoints))
        self.log.append("### Collect XYZ measurement points finished")
        return (xPoints, yPoints, zPoints)


def main():
    log = LogData(logging.INFO)
    terminal = TerminalData(log)
    terminal.printMessage("My first message from TerminalData\n")
    #terminal.getIntegerInput("Measurement points on X axis (2 - 10): ", 2, 10)
    #terminal.getFloatInput("Resolution (2.0 - 10.0): ", 2.0, 10.0)
    terminal.getXYZpoints()
    pass

if __name__ == '__main__':
    main()
