#!/usr/bin/python

import logging
#from LogFile import LogData
#from ParseInput import ParseInput
#from ConfigFile import Configuration
#from EM3Dreprap import RepRap
#from EM3Dnalib import NetworkAnalyzer
#from OutputFile import OutputFile
#from Scanner import Scanner as Scan
#from TerminalData import TerminalData
from src import *


class Scanner(object):
    ''' Main object that will do the scan
    '''
    def __init__(self):
        ''' Set scanner to initial state
        '''
        # set logger
        log = LogData(logging.INFO)
        log.append("Scanner object created")

        # parse input arguments
        inputParser = ParseInput(log)
        arguments = inputParser.getArguments()
        log.append("Parsed arguments (%s) (%s) (%s) (%s)" % arguments)

        # check config file
        #config = Configuration(log, arguments)
        config = Configuration(log, arguments[2])
        log.append("Configuration loaded from file '%s'"
                   % config.CONFIG_FILE_NAME)
        # better visualization in .log file
        log.append("### Configuration finished ")

        self.reprap = RepRap()
        # create RepRap object if enabled
        if arguments[1] == 'enable':
            log.append("RepRap object created ( %s )" % self.reprap)
            rr = config.getRepRapConfig()
            if self.reprap.connect(rr[0], rr[1]):
                log.append("RepRap is online")
                print("RepRap is online")
            else:
                # if cannot connect to reprap
                log.append("Can't connect to RepRap")

        self.pna = NetworkAnalyzer()
        # create Network Analyzer object if selected
        if arguments[0] == 'pna':
            log.append("Network Analyzer object created ( %s )" % self.pna)
            na = config.getPnaConfig()
            if self.pna.connect(na[0], na[1]):
                log.append("PNA is online")
                print("PNA is online")
            else:
                # if cannot connect to pna
                log.append("Can't connect to PNA")

        # set output file name from terminal
        if arguments[3] is not None:
            self.OUTPUT_FILE_NAME = arguments[3]
            log.append("### Output file name set from terminal to ( %s )"
                       % self.OUTPUT_FILE_NAME)
        else:
            self.OUTPUT_FILE_NAME = config.getOutputFileName()
            log.append("### Output file name set from config file to ( %s )"
                       % self.OUTPUT_FILE_NAME)

        # check if connections are OK !

        # get measurement parameters !
        if self.pna.connected or self.reprap.connected:
            terminal = TerminalData(log)
            xyzRes = terminal.getXYZresolution()
            xyzCoords = terminal.getXYZpoints()
        else:
            xyzRes = None
            xyzCoords = None

        # create output file set 'name' and 'device' in header
        if arguments[0] is not None:
            out = OutputFile(log, self.OUTPUT_FILE_NAME, arguments[0])
            # test if everything works ok
            out.createHeader("+20.000e9", "+30.000e10", "+201", "S21",
                            xyzCoords, xyzRes, log.name)
            #out.appendToFile("X:0.00Y:0.00Z:0.00E:0.00",
            #                 "+2.80000000000E+010,+2.80100000000E+010")
        else:
            print "Output file was not created"

        #print arguments[0]

        # create one x row scan to file
        if self.reprap.connected:
            #
            s = Scan(logging=log, rr=self.reprap, na=None,
                     mp=xyzCoords, of=out, step=xyzRes)
            s.mm()
            '''
            for i in range(xyzCoords[1]):
                message = ("G1 Y" + str(xyzCoords[1] + xyzRes[0]) + "\n")
                self.reprap.printer.write(message)
                self.reprap.printer.readline()
                self.reprap.printer.readline()
                s = Scan(logging=log, rr=self.reprap, na=None,
                         mp=xyzCoords, of=out, step=xyzRes)
                log.append("Scan object created")
                s.mX()
            '''

        # disconnect reprap if connected
        # how to disconnect reprap gracefully
        if self.reprap.connected is True:
            self.reprap.disconnect()
            log.append("RepRap is offline")
            print("RepRap is offline")

        # disconnect pna if connected
        # how to disconnect pna gracefully
        if self.pna.connected is True:
            self.pna.disconnect()
            log.append("PNA is offline")
            print("PNA is offline")

        # logging finish
        log.append("Logging finished")


def main():
    scan = Scanner()
    #print scan

if __name__ == '__main__':
    main()
