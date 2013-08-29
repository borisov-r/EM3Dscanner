#import os
import csv
import datetime
import logging
from LogFile import LogData


class OutputFile(object):
    ''' Create output file with header
    '''
    def __init__(self, logging, filename, device):
        ''' Create new file with and header
        '''
        if filename is not None:
            self.OUTPUT_FILE = filename
            self.log = logging
            self.log.append("### Output file creation started")
            self.T = "\n"  # termination character
            #
            # create new file for each measurement
            with open(filename, 'w') as f:
                f.writelines("# Date:           ")
                f.writelines(datetime.datetime.now().isoformat())
                f.writelines(self.T)
                f.writelines("# Device:         " + str(device) + self.T)
                self.log.append("Date and device written to '%s' file"
                                % filename)
        else:
            self.log.append("Output filename set to ( %s )" % filename)
            print("Error output file not set")

    def createHeader(self, minFreq, maxFreq, freqPoints, parameters,
                     xPoints, yPoints, zPoints, resolution,
                     logFileName):
        ''' Update header in output file
        '''
        try:
            with open(self.OUTPUT_FILE, 'a') as f:
                f.writelines("# LOG file:       " + logFileName
                             + self.T)
                f.writelines("# Frequency band: " + minFreq + " : " +
                             maxFreq + self.T)
                f.writelines("# Freq points:    " + freqPoints + self.T)
                f.writelines("# Parameters:     " + parameters + self.T)
                f.writelines("# RepRap points   X Points:   " + str(xPoints) +
                             "   |   Y Points:   " + str(yPoints) +
                             "   |   Z Points:   " + str(zPoints) + self.T)
                f.writelines("# Resolution:     " + resolution + self.T)
                f.writelines("# Volume:         " +
                             str(int(xPoints) * int(yPoints) * int(zPoints)) +
                             self.T)
                self.log.append("PNA header created in output file")
        except IOError, e:
            print e
            self.log.append(e)

    def appendToFile(self, coord, data):
        ''' Append row to output file
                receives two strings 'coords' and 'data'
                coords format: X:0.00Y:0.00Z:0.00E:0.00
                data format:   +2.80000000000E+010,+2.80100000000E+010
        '''
        cc = self.coordinatesToFile(coord)
        dd = data.split(",")
        message = cc + dd
        with open(self.OUTPUT_FILE, 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(message)
            self.log.append("One of CSV 'coord' and 'data' row appended")
        return True

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


def main():
    log = LogData(logging.INFO)
    out = OutputFile(log, 'em3dtst.out', 'pna')
    out.createHeader("+20.000e9", "+30.000e10", "+201", "S21", "10", "10",
                     "10", "0.1", "em3d.log")
    out.appendToFile("X:0.00Y:0.00Z:0.00E:0.00",
                     "+2.80000000000E+010,+2.80100000000E+010")

if __name__ == '__main__':
    main()
