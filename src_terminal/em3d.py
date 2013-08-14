#!/usr/bin/python

import argparse         # get arguments from terminal
import logging
import sys
import os
import xml.etree.ElementTree as ET
import EM3Dnalib
import EM3Dreprap

# Default config file name
CONFIG_FILE_NAME = "em3da.xml"

# Log file name. Should be defined in config file.
LOG_FILE_NAME = None

# Default output file name
OUTPUT_FILE_NAME = "RawData.data"

# Default measurement device
MEASURE_DEVICE = None


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

    args = parser.parse_args()

    if args.measure:
        # chose measurement device
        MEASURE_DEVICE = (args.measure)

    if args.config:
        # check if file existst
        if os.path.exists(args.config):
            CONFIG_FILE_NAME = args.config
            logFileExists = True
        else:
            print "Configuration file not found"
    elif os.path.exists(CONFIG_FILE_NAME):
        logFileExists = True

    if args.log_file:
        LOG_FILE_NAME = args.log_file

    if args.output:
        # set output file name
        OUTPUT_FILE_NAME = (args.output)

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


def main(argv):
    # parse terminal variables
    if parseInput():
        dev = parseConfigFile()
        print dev
        print "LOG_FILE_NAME: " + LOG_FILE_NAME
        removeLogFile(LOG_FILE_NAME)
        logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
        if MEASURE_DEVICE == 'pna':
            logging.info('PNA_IP_ADDRESS = %s', dev[0])
            logging.info('PNA_PORT = %s', dev[1])
            logging.info('CALIB = %s', dev[2])
    else:
        print "No configuration file"
        pass

if __name__ == '__main__':
    main(sys.argv[1:])
