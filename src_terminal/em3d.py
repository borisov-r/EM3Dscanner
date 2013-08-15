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

# Default reprap setting
REPRAP_DEVICE = "None"


def parseInput():
    ''' Get input from command line and parse variables.
    Returns 'True' if configuration file found else returns 'False'
    '''
    # terminal input parser
    global MEASURE_DEVICE
    global REPRAP_DEVICE
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
    parser.add_argument('-rr', '--reprap', choices=['disable', 'enable'],
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
    if args.reprap:
        # enable reprap from terminal
        REPRAP_DEVICE = (args.reprap)
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
            return rr
        else:
            logging.info('RepRap connection error')
            return False
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
        f.writelines("# Resolution:     " + resolution + TERM)
        f.writelines("# Volume:         " +
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
        if value > 0 and value < 5000:
            logging.info('points for axis %s: %s' % (axis, value))
            # logging.info('number of points for %s: %s' % axis % value)
            return value
        else:
            return True
    except ValueError:
        logging.info('Error in askForPoints for %s axis' % axis)
        print "Error please enter positive integer value (1-100000)"
        return True


def askForResolution():
    ''' get raw data from terminal and return value
    '''
    try:
        value = float(raw_input('Enter scan resolution (0.1 - 10 mm): '))
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


def pnaHeader(fileName, networkAnalyzer, points):
    ''' This function adds more info to the data file.
    '''
    #
    # Get all frequencies from the PNA
    idn = networkAnalyzer.getPnaIDN()
    #
    # Get all frequencies for the measurement
    freq = networkAnalyzer.askPna("calc:data:snp?")
    #
    # single frequency is represented with 20 characters received from PNA
    singleFreqChars = 20
    #
    # add header to file
    appendData(fileName, "# PNA idn:        " + idn)
    logging.info("PNA idn appended to file")
    #
    appendData(fileName, "# Format in file: " +
               "|   Reprap points   |" + "   PNA data   |")
    #
    appendData(OUTPUT_FILE_NAME, "#                 " +
               "|      x " + " y " + " z      |" + "    data      |")
    # remove last "'" from the frequency list
    appendData(fileName, "Frequencies:\n"
               + str(freq[0:int(points) * singleFreqChars - 1]) + "\nData:")


def moveRepRapX(reprap, na, window, dir, res, speed,
                pointsX, pointsY, pointsZ):
    ''' Mover RepRap in X direction and show progress
            reprap  - connected reprap object
            na      - network analyzer object
            window  - network analyzer window chosen from terminal
            points  - number point in X direction
            dir     - True / False (forward, backward) direction +/-
            res     - set stepping (resolution in mm)
            speed   - set speed
            pointsX - number of points in X direction
            pointsY - number of points in Y direction
            pointsZ - number of points in Z direction
    '''
    rr = reprap
    device = na
    # x movement of the reprap
    for x in range(pointsX):
        if x is not 0:
            rr.move(ff=dir, moveX=res, speed=speed)
        appendData(OUTPUT_FILE_NAME, "%s %s %s " % (x, pointsY, pointsZ)
                   + device.measureSinglePointAmplitude(None, window))
        logging.info("Measured X point: %s" % x)
        logging.info("X direction set to: %s" % dir)
        #
        # print status in terminal
        sys.stdout.write('\rMeasuring point number: x=%d, y=%d, z=%d'
                         % (x, pointsY, pointsZ))
        sys.stdout.flush()
    sys.stdout.write('\n')
    return True


def moveRepRapY(reprap, na, window, dir, res, speed,
                pointsX, pointsY, pointsZ):
    ''' Mover RepRap in X direction and show progress
            reprap  - connected reprap object
            na      - network analyzer object
            window  - network analyzer window chosen from terminal
            points  - number point in X direction
            dir     - True / False (forward, backward) direction +/-
            res     - set stepping (resolution in mm)
            speed   - set speed
            pointsX - number of points in X direction
            pointsY - number of points in Y direction
            pointsZ - number of points in Z direction
    '''
    rr = reprap
    device = na
    for y in range(pointsY):
        # move y
        if y % 2 == 0:
            # odd number
            direction = True
        else:
            direction = False
        if y is not 0:
            rr.move(ff=dir, moveY=res, speed=speed)
        logging.info("Measure Y point number: %s" % y)
        logging.info("Y direction set to: %s" % dir)
        moveRepRapX(rr, device, window, direction, res, speed,
                    pointsX, y, pointsZ)


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
        # start reprap if enable
        if REPRAP_DEVICE == 'enable':
            rr = reprap(enable=True)
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
            # choose which window to measure from PNA
            window = getPNAwindow()
            #
            # write header in OUTPUT_FILE_NAME
            headerData(OUTPUT_FILE_NAME,
                       xpoints=str(rrPoints[0]),
                       ypoints=str(rrPoints[1]),
                       zpoints=str(rrPoints[2]),
                       points=str(points),
                       resolution=str(resolution),
                       minFreq=minFreq, maxFreq=maxFreq,
                       parameters=parameters)
            #
            # append to OUTPUT_FILE_NAME header for
            # frequencies, idn and file format
            pnaHeader(OUTPUT_FILE_NAME, device, points)
            #
            # calculate number of points
            allPoints = rrPoints[0] * rrPoints[1] * rrPoints[2]
            print("Points to be measured (x * y * z): %s"
                  % allPoints)
            #
            # actual move and measure procedure here
            for z in range(rrPoints[2]):
                if z % 2:
                    direction = False
                else:
                    direction = True
                if z is not 0:
                    rr.move(ff=True, moveZ=resolution, speed=600)
                logging.info("Measure Z point: %s" % z)
                logging.info("Y direction set to: %s" % direction)
                moveRepRapY(rr, device, window, direction, resolution, 600,
                            rrPoints[0], rrPoints[1], z)
            #
            # finish measurement and disconnect from PNA
            if REPRAP_DEVICE == 'enable':
                rr.disconnect()
                logging.info("RepRap disconnected")
    else:
        print "No configuration file"
        pass


if __name__ == '__main__':
    main(sys.argv[1:])
