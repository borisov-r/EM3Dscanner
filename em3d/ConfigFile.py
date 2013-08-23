import os
import logging
from LogFile import LogData
import xml.etree.ElementTree as ET


class Configuration(object):
    ''' Read default configuration file if '-c' argument not passed.
    '''
    def __init__(self, logging, argument):
        ''' logging - pass log object to collect info in log file
            argument - argument passed from terminal
        '''
        self.CONFIG_FILE_NAME = None
        self.log = logging
        #
        if self.checkIfFileExists(argument):
            # configuration file found
            configFileName = self.getFileName(argument)
            self.setConfigFileName(configFileName)
            #
            # reprap configuration is set to 'rr' variable
            self.rr = self.getRepRapConfig()
            #
            # pna configuration is set to 'pna' variable
            self.pna = self.getPnaConfig()
            #
            # atmega configuration is set to 'atmega' variable
            self.atmega = self.getAtmegaConfig()
            #
            # output configuration is set to 'output' variable
            self.out = self.getOutputFileName()
            #
            #
        elif self.checkIfFileExists('em3d.xml'):
            # configuration file not found
            configFileName = self.getFileName('em3d.xml')
            self.setConfigFileName(configFileName)
            self.log.append("File '%s' not found" % argument)
            self.log.append("Using '%s' file for configuration"
                            % self.CONFIG_FILE_NAME)
            #
            # reprap configuration is set to 'rr' variable
            self.rr = self.getRepRapConfig()
            #
            # pna configuration is set to 'pna' variable
            self.pna = self.getPnaConfig()
            #
            # atmega configuration is set to 'atmega' variable
            self.atmega = self.getAtmegaConfig()
            #
            # output configuration is set to 'output' variable
            self.out = self.getOutputFileName()
            #
            #
        else:
            self.log.append("Default configuration file 'em3d.log'" +
                            + "not found")
            print("Error default configuration file not found")
            #
            print("Error configuration file not found")

    def checkIfFileExists(self, name):
        ''' Check if file with given filename exists in the same folder
                return True if file exist
                return False if file does not exist
        '''
        self.log.append("### Checking if '%s' exists" % name)
        if name is None:
            name = 'em3d.xml'
        #
        if os.path.exists(name):
            self.log.append("File '%s' exists" % name)
            return True
        else:
            self.log.append("File '%s' not found" % name)
            return False

    def getFileName(self, name):
        ''' Get name file name assume file exists
        '''
        self.log.append("### Getting config file name '%s'" % name)
        if name is None:
            name = 'em3d.xml'
        #
        if os.path.exists(name):
            self.log.append("Config file name is '%s'" % name)
            return name
        else:
            self.log.append("Config file '%s' not found" % name)
            return False

    def setConfigFileName(self, name):
        ''' This method sets the name of the config file, when checked
            that file exist in the folder
        '''
        self.CONFIG_FILE_NAME = name
        self.log.append("### Configuration file is set to '%s'"
                        % self.CONFIG_FILE_NAME)

    def getRepRapConfig(self):
        ''' Read RepRap configuration from file
        '''
        #
        tree = ET.parse(self.CONFIG_FILE_NAME)
        #
        rrPort = tree.findtext
        rrPort = tree.findtext('./reprap/port')
        rrBaud = tree.findtext('./reprap/baud')
        rrMaxXY = tree.findtext('./reprap/MAX_XY_AXIS')
        rrMaxZ = tree.findtext('./reprap/MAX_Z_AXIS')
        self.log.append(
            "RepRap from file( port(%s), baud(%s), MAX_XY(%s), MAX_Z(%s) )"
            % (rrPort, rrBaud, rrMaxXY, rrMaxZ))
        return (rrPort, rrBaud, rrMaxXY, rrMaxZ)

    def getPnaConfig(self):
        ''' Read PNA configuration from file
        '''
        #
        tree = ET.parse(self.CONFIG_FILE_NAME)
        #
        pnaIp = tree.findtext('./pna/ip')
        pnaPort = tree.findtext('./pna/port')
        pnaCalib = tree.findtext('./pna/calib')
        self.log.append("PNA from file ( ip(%s), port(%s), calib(%s) )"
                        % (pnaIp, pnaPort, pnaCalib))
        return (pnaIp, pnaPort, pnaCalib)

    def getAtmegaConfig(self):
        ''' Read Atmega configuration from file
        '''
        #
        tree = ET.parse(self.CONFIG_FILE_NAME)
        #
        atmegaPort = tree.findtext('./atmega/port')
        atmegaBaud = tree.findtext('./atmega/baud')
        self.log.append("ATmega from file ( port(%s), baud(%s) )"
                        % (atmegaPort, atmegaBaud))
        return (atmegaPort, atmegaBaud)

    def getOutputFileName(self):
        ''' Read Output file name from configuration file
        '''
        #
        tree = ET.parse(self.CONFIG_FILE_NAME)
        #
        output = tree.findtext('./output/file')
        self.log.append("Output from file ( %s )" % output)
        return output


def main():
    log = LogData(logging.INFO)
    # test if None parameter given
    c1 = Configuration(log, None)
    # test if correct name give
    c2 = Configuration(log, 'em3d.xml')
    # test if wrong name given
    c3 = Configuration(log, 'em3da.xml')

if __name__ == '__main__':
    main()
