import LogFile
import logging
import argparse


class ParseInput(object):
    ''' Parse command line input
    '''
    def __init__(self, logging):
        ''' Get logging as input parameter to log
            gathered information in one file
        '''
        # start logging
        self.log = logging

    def getArguments(self):
        ''' Parse arguments from input and return tuple(m, rr, c, o), where:
              m  - takes values {pna, atmega}
              rr - takes values {enable, disable}
              c  - change configuration file
              o  - change output file
        '''
        # parse terminal arguments
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
        self.log.append("Terminal arguments(%s)" % args)
        #
        # measure device --measure
        m = args.measure
        #
        # reprap device --reprap
        rr = args.reprap
        #
        # config file --config
        c = args.config
        #
        # output file --output
        o = args.output
        #
        # m - measure device, rr - reprap, c - cofiguration, o - output
        self.log.append("Parameters from terminal: " +
                        "m(%s) rr(%s) c(%s) o(%s)" % (m, rr, c, o))
        return (m, rr, c, o)


def main():
    log = LogFile.LogData(logging.INFO)
    parser = ParseInput(log)
    log.append(parser.getArguments())

if __name__ == "__main__":
    main()
