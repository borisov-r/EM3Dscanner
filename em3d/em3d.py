import logging
from LogFile import LogData
from ParseInput import ParseInput
from ConfigFile import Configuration
from EM3Dreprap import RepRap
from EM3Dnalib import NetworkAnalyzer
from OutputFile import OutputFile


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

        # create RepRap object if enabled
        if arguments[1] == 'enable':
            self.reprap = RepRap()
            log.append("RepRap object created ( %s )" % self.reprap)

        # create Network Analyzer object if selected
        if arguments[0] == 'pna':
            self.pna = NetworkAnalyzer()
            log.append("Network Analyzer object created ( %s )" % self.pna)

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

        # create output file set 'name' and 'device' in header
        out = OutputFile(log, self.OUTPUT_FILE_NAME, arguments[0])
        # test if everything works ok
        out.createHeader("+20.000e9", "+30.000e10", "+201", "S21", "10", "10",
                         "10", "0.1", log.name)
        out.appendToFile("X:0.00Y:0.00Z:0.00E:0.00",
                         "+2.80000000000E+010,+2.80100000000E+010")

    def test(self):
        pass


def main():
    scan = Scanner()
    print scan

if __name__ == '__main__':
    main()
