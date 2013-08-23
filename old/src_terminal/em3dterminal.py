#!/usr/bin/python

import argparse         # get arguments from terminal
import logging
import sys
import os
import xml.etree.ElementTree as ET
import csv
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
        return (m, rr, c, o)

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
    ''' Create logging object and log everything to file 'em3dterminal.log'

            example: LogData(logging.DEBUG)

            options: logging.DEBUG, logging.INFO, logging.WARNING,
                     logging.ERROR, logging.CRITICAL
        After calling this object you can use:
                     logging.debug('message')
                     logging.info('message')
                     logging.warning('message')
                     logging.error('message')
                     logging.critical('critical')
    '''
    def __init__(self, levelMode):
        logging.basicConfig(filename="em3dterminal.log",
                            level=levelMode, filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s')


class ConfigReader(object):
    ''' Read configuration file
    '''
    def __init__(self):
        pass


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
        LogData(logging.INFO)
        logging.info("Another TEST")
        pass


def main():
    em3d = Scanner()


if __name__ == "__main__":
    main()
