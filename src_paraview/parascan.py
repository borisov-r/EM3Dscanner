import logging
from paraview import *


class parascan:
    """
    Main class for the 3DEMscanner.
    On init, generates Wavelet() object and sets dimensions with WholeExtent().
    This file runs in paraview 3.14.0 or later.

    This class should be able to generate initial wavelet, fetch the data
    from servermanager and transform point data to cell data.
    The generated object should be zeros in CellData for all cells and
    should have dimenssions = xPoints (x) yPoints (x) zPoints.
    """
    def __init__(self):
        self.one = 1               # sets initial cube dimensions
        self.zero = 0              # sets 0 when called

        self.xPoints = self.one    # points to measyre on X axis
        self.yPoints = self.one    # points to measure on Y axis
        self.zPoints = self.one    # points to measure on Z axis
        self.log = logging  # try to get some logging info

        self.wave = Wavelet()
        self.wave.WholeExtent.SetData([self.zero, self.xPoints,
                                       self.zero, self.yPoints,
                                       self.zero, self.zPoints])

        self.wave.XFreq = self.zero
        self.wave.YFreq = self.zero
        self.wave.ZFreq = self.zero
        self.wave.XMag = self.zero
        self.wave.YMag = self.zero
        self.wave.ZMag = self.zero
        self.wave.Maximum = self.zero
        self.wave.StandardDeviation = self.one


if __name__ == '__main__':
    test = parascan()
    y = GetActiveSource()
    RenameSource('MeasuredData')
    Show()
    Render()
