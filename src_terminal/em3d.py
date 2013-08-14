#!/usr/bin/python

import argparse         # get arguments from terminal
import logging
import sys
import os
import xml.etree.ElementTree as ET
import EM3Dnalib
import EM3Dreprap
import datetime

# Default config file name
CONFIG_FILE_NAME = "em3da.xml"

# Log file name. Should be defined in config file.
LOG_FILE_NAME = None

# Default output file name
OUTPUT_FILE_NAME = "RawData.data"

# Default measurement device
MEASURE_DEVICE = "None"


def parseInput():
    ''' Get input from command line and parse variables.
    Returns 'True' if configuration file found else returns 'False'
    '''
    # terminal input parser
    global MEASURE_DEVICE
    global OUTPUT_FILE_NAME
    global CONFIG_FILE_NAME
    global LOG_FILE_NAME
    #
    logFileExists = False
    #
    parser = argparse.ArgumentParser(description='EM3D scanner suite')
    parser.add_argument('-m', '--measure', choices=['pna', 'atmega'],
                        help=
                        'Choose device for the measurement. Default: None')
    parser.add_argument('-c', '--config',
                        help=
                        'Set configuration file name. Default: "em3da.xml"')
    parser.add_argument('-l', '--log-file',
                        help=
                        'Set log file name. Default: "EM3Dscanner.log"')
    parser.add_argument('-o', '--output',
                        help='Output file name. Default: "RawData.data"')
    #
    args = parser.parse_args()
    #
    if args.measure:
        # chose measurement device
        MEASURE_DEVICE = (args.measure)
    #
    if args.config:
        # check if file existst
        if os.path.exists(args.config):
            CONFIG_FILE_NAME = args.config
            logFileExists = True
        else:
            print "Configuration file not found"
    elif os.path.exists(CONFIG_FILE_NAME):
        logFileExists = True
    #
    if args.log_file:
        LOG_FILE_NAME = args.log_file
    #
    if args.output:
        # set output file name
        OUTPUT_FILE_NAME = (args.output)
    #
    if logFileExists:
        return True
    else:
        return False


def parseConfigFile(name=CONFIG_FILE_NAME):
    ''' Parse configuration file and returns tuple of
        measurement device parameters.
    '''
    #
    global LOG_FILE_NAME
    tree = ET.parse(name)
    #
    if LOG_FILE_NAME is None:
        LOG_FILE_NAME = tree.findtext('./log/log-file')

    if MEASURE_DEVICE == 'pna':
        # return (IP, PORT, CALIB) of the PNA
        pnaIp = tree.findtext('./pna/ip')
        pnaPort = tree.findtext('./pna/port')
        pnaCalib = tree.findtext('./pna/calib')
        return (pnaIp, pnaPort, pnaCalib)
    elif MEASURE_DEVICE == 'atmega':
        atmegaPort = tree.findtext('./atmega/port')
        atmegaBaud = tree.findtext('./atmega/baud')
        return (atmegaPort, atmegaBaud)
    else:
        return None


def removeLogFile(name=LOG_FILE_NAME):
    # check if log file exists and dete it
    if os.path.exists(name):
        os.remove(name)
        return True
    else:
        return False


def startLogging(dev, file, lvl=logging.INFO):
    ''' Start logging to file. Returns True.
    '''
    logging.basicConfig(filename=file, level=lvl,
                        format='%(asctime)s %(levelname)s %(message)s')
    if MEASURE_DEVICE == 'pna':
        logging.info('Using device: %s', MEASURE_DEVICE)
        logging.info('PNA ip address:  %s', dev[0])
        logging.info('PNA port: %s', dev[1])
        logging.info('PNA calibration: %s', dev[2])
    elif MEASURE_DEVICE == 'atmega':
        logging.info('Using device: %s', MEASURE_DEVICE)
        logging.info('ATMEGA port:  %s', dev[0])
        logging.info('ATMEGA baud:  %s', dev[1])
    return True


def connect(device, parameters):
    ''' Connect to device. Returns: object of the connected device.
    '''
    if device == 'pna':
        pna = EM3Dnalib.NetworkAnalyzer()
        try:
            pna.connect(parameters[0], parameters[1])
            logging.info('Connected to PNA')
            return pna
        except:
            logging.info('Error while connecting to PNA')
            return False
    elif device == 'atmega':
        # this option is not available for now
        logging.info('This option is not available still.')
        return False


def reprap(p='/dev/ttyACM0', b='115200', enable=False):
    ''' Connect to reprap and test movements.
    '''
    if enable:
        rr = EM3Dreprap.RepRap()
        if rr.connect(port=p, baudrate=b):
            logging.info('Connected to RepRap')
        else:
            logging.info('RepRap connection error')
        rr.move(False, 10)
        rr.disconnect()
        return True
    else:
        logging.info('RepRap disabled')
        pass


def headerData(fileName, minFreq="0", maxFreq="1", points="1",
               xpoints="0", ypoints="0", zpoints="0",
               resolution="0.1", parameters='S21'):
    ''' Take data from PNA write it to file.
        fileName    - output file name (OUTPUT_FILE_NAME)
        parameters  - stored data parameters
        minFreq     - when used PNA low frequency, default = 0
        maxFreq     - when used PNA high frequency, default = 1
        points      - network analyzer measurement points, default = 1
        parameters  - measured parameters, default = S21
        xpoints, ypoints, zpoints - x, y, z reprap points
        xpoints * ypoints * zpoints = volume - measured volume
    '''
    global LOG_FILE_NAME
    global MEASURE_DEVICE
    TERM = '\n'
    # open file if not found create one
    # after finish writing to file closes automatically
    with open(fileName, 'w+') as f:
        f.writelines("# Date:           ")
        f.writelines(datetime.datetime.now().isoformat())
        f.writelines(TERM)
        f.writelines("# Device:         " + MEASURE_DEVICE + TERM)
        f.writelines("# LOG file:       " + LOG_FILE_NAME + TERM)
        f.writelines("# Frequency band: " + minFreq + " : " + maxFreq + TERM)
        f.writelines("# Freq points:    " + points + TERM)
        f.writelines("# Parameters:     " + parameters + TERM)
        f.writelines("# RepRap points:  X Points:   " + xpoints +
                     "   |   Y Points:   " + ypoints +
                     "   |   Z Points:   " + zpoints + TERM)
        f.writelines("# Resolution      " + resolution + TERM)
        f.writelines("# Volume          " +
                     str(int(xpoints) * int(ypoints) * int(zpoints)) + TERM)


def appendData(fileName, data):
    """ Append data lines to file.
    """
    TERM = '\n'
    with open(fileName, 'a') as f:
        f.writelines(data + TERM)


def askForPoints(axis):
    ''' get raw data from terminal and return value
    '''
    try:
        value = int(raw_input('Enter number of points for %s axis: ' % axis))
        logging.info('points for axis %s: ' % axis)
        logging.info('got value: %s' % value)
        return value
    except ValueError:
        logging.info('Error in askForPoints for %s axis' % axis)
        print "Error please enter positive integer value (1-100000)"
        return True


def askForResolution():
    ''' get raw data from terminal and return value
    '''
    try:
        value = float(raw_input('Enter scan resolutin: '))
        logging.info('scan resolution: %s' % value)
        return value
    except ValueError:
        logging.info('Error in resolution value')
        print "Error please enter positive integer value (0.1-10 mm)"
        return True


def askForPNAwindow():
    ''' get raw data from terminal and return value
    '''
    try:
        value = int(raw_input('Select PNA window for the measurement (1-4): '))
        if value > 0 and value < 5:
            logging.info('PNA window selected: %s' % value)
            logging.info('got value: %s' % value)
            return value
        else:
            return True
    except ValueError:
        logging.info('Error in askForPoints')
        print "Error please enter positive integer value (1-4)"
        return True


def getMeasurementPoints():
    ''' Get x, y, z points for the measurement.
    '''
    # X axis points
    while True:
        xpoints = askForPoints("X")
        if xpoints is not True:
            break
    # Y axis points
    while True:
        ypoints = askForPoints("Y")
        if xpoints is not True:
            break
    # Z axis points
    while True:
        zpoints = askForPoints("Z")
        if xpoints is not True:
            break
    #
    return (xpoints, ypoints, zpoints)


def getResolution():
    ''' Ask for required resolution in terminal and set it. Returns value.
    '''
    while True:
        resolution = askForResolution()
        if resolution is not True:
            break
    #
    return (resolution)


def getPNAwindow():
    ''' Get x, y, z points for the measurement.
    '''
    # X axis points
    while True:
        window = askForPNAwindow()
        if window is not True:
            break
    #
    return (window)


def main(argv):
    # parse terminal variables
    if parseInput():
        deviceParameters = parseConfigFile()
        print "EM3D scanner started"
        print "DEVICE: " + MEASURE_DEVICE
        print "Parameters: "
        print deviceParameters
        print "Log file name: " + LOG_FILE_NAME
        # remove old log files before start
        removeLogFile(LOG_FILE_NAME)
        # start logging
        startLogging(deviceParameters, LOG_FILE_NAME)
        #
        device = connect(MEASURE_DEVICE, deviceParameters)
        #
        reprap()
        #
        # Data points for X, Y, Z from terminal
        # Returns: tuple(xpoints, ypoints, zpoints)
        rrPoints = getMeasurementPoints()
        resolution = getResolution()
        logging.info("Points from terminal: " + str(rrPoints))
        #
        if MEASURE_DEVICE == 'pna':
            print device.getPnaIDN()
            freq = device.getFrequencyRange()
            points = device.getNumberOfMeasurementPoints()
            parameters = device.askPna("calc:par:cat?")
            minFreq = freq[0:(len(freq) / 2)]
            maxFreq = freq[(len(freq) / 2) + 1:len(freq)]
            # Data file header
            #
            headerData(OUTPUT_FILE_NAME,
                       xpoints=str(rrPoints[0]),
                       ypoints=str(rrPoints[1]),
                       zpoints=str(rrPoints[2]),
                       points=str(points),
                       resolution=str(resolution),
                       minFreq=minFreq, maxFreq=maxFreq,
                       parameters=parameters)
            #
            window = getPNAwindow()
            for p in range(3):
                appendData(OUTPUT_FILE_NAME,
                           device.measureSinglePointAmplitude(None, window))
                logging.info("Measured point number: %s" % p)
    else:
        print "No configuration file"
        pass


if __name__ == '__main__':
    main(sys.argv[1:])
