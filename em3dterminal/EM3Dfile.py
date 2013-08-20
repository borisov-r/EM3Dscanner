#!/usr/bin/env python

#==============================================================================
# 3DEMnalib.py is part of 3DEMscanner suit software.
#
# 3DEMscanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ParaScan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Printrun. If not, see <http://www.gnu.org/licenses/>
#==============================================================================

""" Filename: EM3Dfile.py

    This file contains class EM3Dfile with following functions:
        __init__(self, filename)
        createHeader(self)
        appendToFile(self)
        csvReader(self)             - read output file and print line by line

"""
import csv
import datetime
import logging


class EM3Dfile(object):
    ''' Main class to handle output file of em3dterminal
            EM3Dfile('filename.out', 'pna', 'logFileName.log')
            device - pna or atmega from console
            logFileName - name of the logging file
    '''
    def __init__(self, filename, device, log,
                 logFileName='em3dterminal.log'):
        self.log = log  # logging to file
        self.LOG_FILE_NAME = logFileName
        self.T = "\n"  # termination character
        # create new file each time when EM3Dfile is called
        if filename is not None:
            self.OUTPUT_FILE = filename
            with open(filename, 'w') as f:
                f.writelines("# Date:           ")
                f.writelines(datetime.datetime.now().isoformat())
                f.writelines(self.T)
                f.writelines("# Device:         " + device + self.T)
                self.log.append("Date and device written output file")
        else:
            print("Output file not defined")
            self.log.append("Output file not defined")

    def createHeader(self, minFreq, maxFreq, points, parameters,
                     xPoints, yPoints, zPoints, resolution):
        ''' Creates header information in the output file
        '''
        try:
            with open(self.OUTPUT_FILE, 'a') as f:
                f.writelines("# LOG file:       " + self.LOG_FILE_NAME
                             + self.T)
                f.writelines("# Frequency band: " + minFreq + " : " +
                             maxFreq + self.T)
                f.writelines("# Freq points:    " + points + self.T)
                f.writelines("# Parameters:     " + parameters + self.T)
                f.writelines("# RepRap points:  X Points:   " + xPoints +
                             "   |   Y Points:   " + yPoints +
                             "   |   Z Points:   " + zPoints + self.T)
                f.writelines("# Resolution:     " + resolution + self.T)
                f.writelines("# Volume:         " +
                             str(int(xPoints) * int(yPoints) * int(zPoints)) +
                             self.T)
                self.log.append("PNA header created in output file")
        except IOError, e:
            print e
            self.log.append(e)

    def coordinatesToFile(self, coords):
        ''' Change format of the coordinates from RepRap to CSV.
                coor format: X:0.00Y:0.00Z:0.00E:0.00
                return string with tabs
        '''
        c = coords.strip()
        self.log.append("Input coordinates: %s" % c)
        x = c.translate(None, "XYZE")
        y = x[1:]   # remove first string ":"
        z = y[0:len(y) - 5]     # remove extruder coordinates
        sp = z.split(":")
        self.log.append("Output coordinates: %s" % sp)
        return sp

    def appendToFile(self, coord, data):
        ''' Append row to output file
                receives two strings 'coords' and 'data'
                data format: +2.80000000000E+010,+2.80100000000E+010
        '''
        dd = data.split(",")
        cc = self.coordinatesToFile(coord)
        message = cc + dd
        with open(self.OUTPUT_FILE, 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(message)
            self.log.append("One of CSV 'coord' and 'data' row appended")
        pass

    def csvReader(self):
        try:
            with open(self.OUTPUT_FILE, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    print row
        except IOError:
            print "Set output file !"
            self.log.append("IOError in csvReader()")


class LogData(object):
    ''' Create logging object and log everything to file 'em3dterminal.log'

            example: LogData(logging.DEBUG)

            options: logging.DEBUG, logging.INFO, logging.WARNING,
                     logging.ERROR, logging.CRITICAL

            After calling this object you can use:
                    log = LogData(logging.INFO
                     debug('message')
                     logging.info('message')
                     logging.warning('message')
                     logging.error('message')
                     logging.critical('critical')
    '''
    def __init__(self, levelMode):
        # start logging file
        self.level = levelMode
        print self.level
        logging.basicConfig(filename="em3dterminal.log",
                            level=levelMode, filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s')
        logging.info("Logging started")

    def append(self, message):
        # append message to log file
        #
        # logging.DEBUG
        if self.level == 10:
            logging.debug(message)
        #
        # logging.INFO
        elif self.level == 20:
            logging.info(message)
        #
        # logging.WARNING
        elif self.level == 30:
            logging.warning(message)
        #
        # logging.ERROR
        elif self.level == 40:
            logging.error(message)
        #
        # logging.CRITICAL
        elif self.level == 50:
            logging.critical(message)
        #
        else:
            pass


def main():
    log = LogData(logging.CRITICAL)
    cf = EM3Dfile('em3d.out', 'pna', log)
    cf.createHeader("2.9GHz", "3.0GHz", "+201", "S21", "31", "21", "41", "5")
    cf.csvReader()
    cf.appendToFile("X:0.10Y:5.00Z:0.00E:0.00", "+3.002,-31.431e10")
    log.append("info message")
    pass


if __name__ == '__main__':
    main()
