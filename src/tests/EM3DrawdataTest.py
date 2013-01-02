class RawDataGenerator(object):
    """ Main class for putting raw data measured from pna to single file.

    File format should look like this:
        * 5 rows - service information, should start with "!"
            ! Raw data from measurement on:
            ! date: 24.10.2012 | time: 11:40
            ! parameters: S21 | amplitude | phase
            ! frequency range: +1.00000000000E+010;+1.01000000000E+010 | points: +2
            ! comments: some info about the measurement
        After first 3 rows data should start with:
        * (x, y, z) | { tuple of raw data for this point }
    """
