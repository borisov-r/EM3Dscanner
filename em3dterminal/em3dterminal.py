#!/usr/bin/python

import argparse         # get arguments from terminal
import logging
#import sys
import os
import EM3Dnalib
import EM3Dreprap
import EM3Dfile
#import datetime


class InputParser(object):
    ''' Parse input from console
    '''
    def __init__(self, logFileName):
        ''' Initial state
        '''
        self.log = logFileName
        self.parsedInput = self.parseArguments()

    def parseArguments(self):
        parser = argparse.ArgumentParser(description='EM3D scanner suite')
        # select measurement device
        parser.add_argument('-m', '--measure', choices=['pna', 'atmega'],
                            help=
                            'Choose device for the measurement. Default: None')
        parser.add_argument('-rr', '--reprap', choices=['disable', 'enable'],
                            help=
                            'Choose device for the measurement. Default: None')
        parser.add_argument('-c', '--config',
                            help=
                            'Set configuration file. Default: "em3da.xml"')
        parser.add_argument('-o', '--output',
                            help='Output file. Default: "RawData.data"')
        #
        args = parser.parse_args()
        #
        # measure device --measure
        m = args.measure
        #
        # reprap device --reprap
        rr = args.reprap
        #
        # config file --config
        c = self.parseConfigFile(args)
        #
        # output file --output
        o = self.parseOutputFile(args)
        #
        # m - measure device, rr - reprap, c - cofiguration, o - output
        self.log.append("Parameters from terminal: " +
                        "m(%s) rr(%s) c(%s) o(%s)" % (m, rr, c, o))
        return (m, rr, c, o)

    def parseConfigFile(self, args):
        ''' parse config file --config
        '''
        if args.config:
            if os.path.exists(args.config):
                c = args.config
                self.log.append("Configuration file found")
            else:
                c = args.config
                self.log.append("Configuration file not found")
                print("Configuration file not found")
        else:
            c = None
            self.log.append("Configuration file is set to: %s" % c)
        return c

    def parseOutputFile(self, args):
        ''' parse output file --output
        '''
        if args.output:
            # set output file name
            if os.path.exists(args.output):
                os.remove(args.output)
                o = args.output
                self.log.append("Old output file was found and was deleted")
                print("Old output file was found and was deleted")
            else:
                o = args.output
                self.log.append("Output file is: %s" % args.output)
        else:
            o = None
            self.log.append("Output file is set to: %s" % o)
        return o


class Scanner(object):
    ''' Class to create EM scan from cosole
    '''
    def __init__(self):
        ''' Initial state of the scanner.
                1. Create log file 'em3dterminal.log'.
                2. Parse inputs.
                3. ...
        '''
        #
        # start logging before anything else started
        log = EM3Dfile.LogData(logging.INFO)
        #
        # read input on start
        #   ( MEASURE_DEVICE,    REPRAP       , CONFIG, OUTPUT )
        #   (  {pna,atmega} , {enable/disable}, CONFIG, OUTPUT )
        c = InputParser(log)
        catchTerminal = c.parsedInput
        #
        # set
        # 'deviceEnable', 'reprapEnable', 'configEnable' and 'outputEnable'
        # from terminal
        self.deviceEnable = catchTerminal[0]
        self.reprapEnable = catchTerminal[1]
        self.configEnable = catchTerminal[2]
        self.outputEnable = catchTerminal[3]
        #
        print catchTerminal
        #
        #
        c = EM3Dfile.ConfigReader(log)
        cfe = c.checkIfConfigFileExists(self.outputEnable)
        # read configuration from file
        if self.configEnable is not None and cfe is True:
            device = c.parseDeviceFromConfigFile(self.deviceEnable,
                                                 self.configEnable)
            reprap = c.parseRepRapFromConfigFile(self.reprapEnable,
                                                 self.configEnable)
            log.append("Parsed data from config file: " +
                       "device(%s), reprap(%s)" % (device, reprap))
        elif cfe is True:
            c = EM3Dfile.ConfigReader(log)
            device = c.parseDeviceFromConfigFile(self.deviceEnable)
            reprap = c.parseRepRapFromConfigFile(self.reprapEnable)
            log.append("Parsed data from config file: " +
                       "device(%s), reprap(%s)" % (device, reprap))
        else:
            print("Configuration file not found")
        #
        # current configuration is set now in device and reprap variables
        #
        #
        #
        #
        #
        #
        # Read configuration file
        '''
        con = ConfigReader(log)
        devParams = con.parseDeviceFromConfigFile(config[0])
        reprapParams = con.parseRepRapFromConfigFile(config[1])
        if devParams is not None:
            logging.info("Parameters read from file len: %s" % len(devParams))
        #
        # Start RepRap if 'enable'
        if config[1] == 'enable':
            self.reprap(enable=True)
        #
        #
        device = self.connect(config[0], devParams)
        print device
        #
        # Data points for X, Y, Z from terminal
        # Returns: tuple(xpoints, ypoints, zpoints)
        if device is not False and device == 'pna':
            rrPoints = self.getMeasurementPoints()
            resolution = self.getResolution()
            logging.info("Points from terminal: " + str(rrPoints))
        #
        # Connect to pna
        if device is not False and\
           config[0] == 'pna' and config[1] == 'enable':
                window = self.askForPNAwindow()
                print device.getPnaIDN()
                print window
                freq = device.getFrequencyRange()
                points = device.getNumberOfMeasurementPoints()
                parameters = device.askPna("calc:par:cat?")
                minFreq = self.freq[0:(len(freq) / 2)]
                maxFreq = self.freq[(len(freq) / 2) + 1:len(freq)]
                #
                # set output file from console
                out = EM3Dfile.EM3Dfile(config[3], config[0], log)
                # create header
                out.createHeader(minFreq, maxFreq, points, parameters,
                                 rrPoints[0], rrPoints[1], rrPoints[2],
                                 resolution)
                #
                out.appendToFile("X:0.00Y:0.00Z:0.00E:0.00",
                                 "+2.80000000000E+010,+2.80100000000E+010")
        #
        # finish measurement and disconnect from PNA
        if device == 'enable':
            #rr.disconnect()
            logging.info("RepRap disconnected")
        '''
        log.append("Logging stoped")
        pass

    def start(self):
        ''' Main function that should be started in __init__ method
        '''
        #

        pass

    def reprap(self, p='/dev/ttyACM0', b='115200', enable=False):
        ''' Connect to reprap and test movements.
        '''
        if enable:
            rr = EM3Dreprap.RepRap()
            if rr.connect(port=p, baudrate=b):
                self.log.append('Connected to RepRap')
                return rr
            else:
                self.log.append('RepRap connection error')
                return False
        else:
            self.log.append('RepRap disabled')
            pass

    def connect(self, device, parameters):
        ''' Connect to device. Returns: object of the connected device.
        '''
        if device == 'pna':
            pna = EM3Dnalib.NetworkAnalyzer()
            try:
                if pna.connect(parameters[0], parameters[1]):
                    logging.info('Connected to PNA')
                    return pna
                else:
                    logging.info('Error while connecting to PNA')
                    return False
            except:
                logging.info('Error while connecting to PNA')
                return False
        elif device == 'atmega':
            # this option is not available for now
            logging.info('This option is not available still.')
            return False

    def askForPNAwindow(self):
        ''' get raw data from terminal and return value
        '''
        try:
            value = int(raw_input('Select PNA window for the' +
                                  ' measurement (1-4): '))
            if value > 0 and value < 5:
                logging.info('PNA window selected: %s' % value)
                return value
            else:
                return True
        except ValueError:
            logging.info('Error in askForPoints')
            print "Error please enter positive integer value (1-4)"
            return True

    def askForPoints(self, axis):
        ''' get raw data from terminal and return value
        '''
        try:
            value = int(raw_input('Enter number of points for %s axis: '
                                  % axis))
            if axis == 'Z':
                if value > 0 and value < self.MAX_Z_AXIS:
                    logging.info('points for axis %s: %s' % (axis, value))
                    return value
                else:
                    logging.info('Error in askForPoints for %s axis' % axis)
                    print("Error please enter positive integer value (1-%s)"
                          % self.MAX_Z_AXIS)
                    return True
            elif value > 0 and value < self.MAX_XY_AXIS:
                logging.info('points for axis %s: %s' % (axis, value))
                #logging.debug('number of points for %s: %s' % (axis, value))
                return value
            else:
                logging.info('Error in askForPoints for %s axis' % axis)
                print("Error please enter positive integer value (1-%s)"
                      % self.MAX_XY_AXIS)
                return True
        except ValueError:
            logging.info('Error in askForPoints for %s axis' % axis)
            print "Error please enter positive integer value (1-100000)"
            return True

    def askForResolution(self):
        ''' get raw data from terminal and return value
        '''
        try:
            value = float(raw_input('Enter scan resolution (0.1 - 200 mm): '))
            if (value > 0.09) and (value < 200.0):
                # check if value is float from 0.1 to 200.0
                logging.info('scan resolution: %s' % value)
                return value
            else:
                logging.info('Error in resolution value')
                print "Error please enter positive integer value (0.1-200 mm)"
                return True
        except ValueError:
            logging.info('Error in resolution value')
            print "Error please enter positive integer value (0.1-200 mm)"
            return True

    def getPNAwindow(self):
        ''' Get x, y, z points for the measurement.
        '''
        # X axis points
        while True:
            window = self.askForPNAwindow()
            if window is not True:
                break
        #
        return (window)

    def getResolution(self):
        ''' Ask for required resolution in terminal and set it. Returns value.
        '''
        while True:
            resolution = self.askForResolution()
            if resolution is not True:
                break
        #
        return (resolution)

    def getMeasurementPoints(self):
        ''' Get x, y, z points for the measurement.
        '''
        # X axis points
        while True:
            xpoints = self.askForPoints("X")
            if xpoints is not True:
                break
        # Y axis points
        while True:
            ypoints = self.askForPoints("Y")
            if ypoints is not True:
                break
        # Z axis points
        while True:
            zpoints = self.askForPoints("Z")
            if zpoints is not True:
                break
        #
        return (xpoints, ypoints, zpoints)


def main():
    Scanner()


if __name__ == "__main__":
    main()
