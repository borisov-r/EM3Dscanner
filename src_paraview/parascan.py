# references: http://www.paraview.org/Wiki/Python_Programmable_Filter
from paraview.simple import *
from paraview import vtk
from logging import *


class Parascan:
    """
    Main class for the 3DEMscanner.
    On init, generates Wavelet() object and sets dimensions with WholeExtent().
    This file runs in paraview 3.14.0 or later.

    This class should be able to generate initial wavelet, fetch the data
    from servermanager and transform point data to cell data.
    The generated object should be zeros in CellData for all cells and
    should have dimenssions = xPoints (x) yPoints (x) zPoints.
    """
    def __init__(self, fileName):
        """
        On __init__ creates log file in DEBUG level.
        """
        self.log = getLogger('parascan')
        self.log.setLevel(DEBUG)
        fh = FileHandler(fileName)
        fh.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.log.addHandler(fh)

        # main program starts here
        self.one = 1               # sets initial cube dimensions
        self.zero = 0              # sets 0 when called

        self.xPoints = self.one    # points to measyre on X axis
        self.yPoints = self.one    # points to measure on Y axis
        self.zPoints = self.one    # points to measure on Z axis

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
        self.log.info('Wavelet with dimensions %s generated.',
                      self.wave.WholeExtent.GetData())


if __name__ == '__main__':
    test = Parascan('parascan.log')
    a = GetActiveSource()
    b = servermanager.Fetch(a)
    pd = b.GetPointData().GetScalars().SetName('Amplitude')
    proba = vtk.vtkFloatArray()
    proba.SetName('Proba')
    proba.SetNumberOfComponents(1)
    test1 = b.GetCellData().AddArray(proba)
    Show()
    RenameSource('MeasuredData')
    Render()
