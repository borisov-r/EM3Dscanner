from datetime import datetime
# from EM3Dnalib import NetworkAnalyzer
# from EM3Dreprap import RepRap


class RawDataGenerator(object):
    """ Main class for putting raw data measured from pna to single file.

    File format should look like this:
        * 5 rows - service information, should start with "!"
            ! Raw data from measurement on:
            ! date: 2012-10-24 15:50:24.652545
            ! parameter: S21 | amplitude | phase
            ! frequency range: +1.00000000000E+010;+1.01000000000E+010 | points: +2
            ! comments: some info about the measurement
        After first 5 rows data should be in collected in following format:
            * (x, y, z) | frequency | { amplitude tuple of raw data for this point }
                                      { phase tuple of raw data for this point }
    """
    def __init__(self, pna=None, reprap=None):
        self.pna = pna
        self.reprap = reprap
        self.measuredParamter = None
        self.measureAmplitude = False  # if True measure amplitude
        self.measurePhase = False  # if True measure phase

    def generateHeader(self, measuredParameter="None",
                       amplitude="None", phase="None"):
        """ This method generates measurement file header.
        If You are going to measure S21 and want both Amplitude and Phase
        measurements this method should be called like this:
            self.generateHeader("S21", "Amplitude", "Phase")
        """
        firstRow = "! Raw data measurement"
        now = datetime.now()
        secondRow = "! Date: " + str(now)
        if "S21" in measuredParameter:
            self.measuredParamter = measuredParameter
        if "Amplitude" in amplitude:
            self.measureAmplitude = True
        if "Phase" in phase:
            self.measurePhase = True
        thirdRow = "! " + measuredParameter + " | " + amplitude + " | " + phase
        print firstRow
        print secondRow
        print thirdRow
        print "init parameter: ", self.measuredParamter
        print "init amplitude: ", self.measureAmplitude
        print "init phase: ", self.measurePhase


def main():
    testObj = RawDataGenerator()
    testObj.generateHeader()
    testObj.generateHeader("S21", "Amplitude", "Phase")

if __name__ == "__main__":
    main()
