#!/usr/bin/python

import argparse         # get arguments from terminal
import logging
import sys
import os
import xml.etree.ElementTree as ET
import EM3Dnalib
import EM3Dreprap
import datetime


class ParseInput(object):
    ''' Parse input from console
    '''
    def __init__(self):
        ''' Initial state
        '''
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
                            'Set configuration file name. Default: "em3da.xml"')
        parser.add_argument('-l', '--log-file',
                            help=
                            'Set log file name. Default: "EM3Dscanner.log"')
        parser.add_argument('-o', '--output',
                            help='Output file name. Default: "RawData.data"')
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
        # log file --log-file
        l = self.parseLogFile(args)
        #
        # output file --output
        o = self.parseOutputFile(args)
        #
        # m - measure device, rr - reprap, c - cofiguration, l - log, o - output
        return (m, rr, c, l, o)

    def parseConfigFile(self, args):
        ''' parse config file --config
        '''
        if args.config:
            if os.path.exists(args.config):
                c = args.config
                print("Configuration file found")
            else:
                c = args.config
                print("Configuration file not found")
        else:
            c = None
        return c

    def parseLogFile(self, args):
        ''' parse log-file
        '''
        if args.log_file:
            if os.path.exists(args.log_file):
                os.remove(args.log_file)
                l = args.log_file
                print("Old log file was found and was deleted")
            else:
                l = args.log_file
                print("Old log file was not found")
        else:
            l = None
        return l

    def parseOutputFile(self, args):
        ''' parse output file
        '''
        if args.output:
            # set output file name
            if os.path.exists(args.output):
                os.remove(args.output)
                o = args.output
                print("Old output file was found and was deleted")
            else:
                o = args.output
        else:
            o = None
        return o


class LogData(object):
    ''' Create logging object and log everything to file
    '''
    def __init__(self, fileName, level=logging.INFO):
        if fileName is not None:
            logging.basicConfig(filename=fileName, level=level,
                                format='%(asctime)s %(levelname)s %(message)s')
        elif fileName is None:
            logging.basicConfig(filename='temp.log', level=level,
                                format='%(asctime)s %(levelname)s %(message)s')
        else:
            pass


class ConfigReader(object):
    ''' Read configuration file
    '''
    def __init__(self, fileName):
        if fileName is not None:
            tree = ET.parse(fileName)


class Scanner(object):
    ''' Class to create EM scan from cosole
    '''
    def __init__(self):
        ''' Initial state of the scanner
                if log file not set from console,
                everything is logged in 'temp.log' file
        '''
        # get input from console
        CONFIG_FILE_NAME = None
        LOG_FILE_NAME = None
        OUTPUT_FILE_NAME = None
        configuration = ParseInput()
        print configuration.parsedInput
        logFile = configuration.parsedInput[3]
        LogData(logFile)
        logging.info("Another TEST")
        pass


def main():
    em3d = Scanner()


if __name__ == "__main__":
    main()
