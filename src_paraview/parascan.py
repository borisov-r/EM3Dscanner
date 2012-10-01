# references: http://www.paraview.org/Wiki/Python_Programmable_Filter
from paraview.simple import *
from paraview import vtk
from logging import *


class Parascan(object):
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
            self.Object - current wavelet object
            self.Data - data Fetched from servermanager (real data)
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

        self.Object = GetActiveSource()
        self.log.info('Active Object set %s', self.Object)
        self.Data = servermanager.Fetch(self.Object)
        self.log.info('Active Data set %s', self.Data)
        # set data file pointer for the writer
        self.writer = self.zero

    def SetScalarsName(self, name):
        """
        This function gets current object Fetch() the date from it and sets
        the name of the current data for PointData().

        example: GetSourceAndSetName('Amplitude')
        """
        self.Data.GetPointData().GetScalars().SetName(name)
        self.log.info('Data with name %s set.', name)

    def AddVtkFloatArrayToSource(self, numberOfComponents, name):
        """
        This function adds to the current source array with integer components
        and set the name property of the array.

        example: AddVtkFloatArrayToSource(100, 'Phase')
        """
        scalars = self.Data.GetNumberOfScalarComponents()
        self.Data.SetNumberOfScalarComponents(scalars + self.one)
        array = vtk.vtkFloatArray()
        array.SetNumberOfComponents(self.one)
        self.log.info('Array parameter NumberOfComponents set to %d',
                      numberOfComponents)
        array.SetNumberOfTuples(numberOfComponents)
        self.log.info('Array parameter NumberOfComponents set to %d',
                      numberOfComponents)
        array.SetName(name)

        for i in range(numberOfComponents):
            array.SetComponent(numberOfComponents, self.zero, 0.0)

        # self.log.info('First component set to: %s', array.GetComponent(0, 0))
        self.log.info('Array name set to %s', name)
        self.Data.GetPointData().AddArray(array)
        self.log.info('Array addded to currentData.')

    def WriteToPVDFile(self, dataMode, name):
        """
        Write data to .pvd file.
        # The mode uses for writing the file's data i.e.
        # ascii = 0, binary = 1, appended binary = 2.
        example: WriteToPVDFile(0, 'test.pvd')
        """
        self.writer = servermanager.writers.XMLPVDWriter(FileName=name, DataMode=dataMode)
        self.writer.Input = self.Object
        self.writer.UpdatePipeline()


def main():
    test = Parascan('parascan.log')
    test.SetScalarsName('Amplitude')
    test.AddVtkFloatArrayToSource(8, 'Phase')
    test.log.info('test Data is: %s', test.Data)
    # print test.Data
    view = servermanager.CreateRenderView()
    servermanager.CreateRepresentation(test.Object, view)
    Show()
    RenameSource('MeasuredData')
    Render()
    test.log.info('test.Data object is: %s', test.Data)
    test.log.info('Number of Arrays in test.Data: %s',
                  test.Data.GetPointData().GetNumberOfArrays())
    test.log.info('First Array 0 name is: %s',
                  test.Data.GetPointData().GetArrayName(0))
    test.log.info('Second Array 1 name is: %s',
                  test.Data.GetPointData().GetArrayName(1))
    test.log.info('Get number of tuples, array0: %s',
                  test.Data.GetPointData().GetArray(0).GetNumberOfTuples())
    test.log.info('Get number of tuples, array1: %s',
                  test.Data.GetPointData().GetArray(1).GetNumberOfTuples())
    test.WriteToPVDFile(test.zero, 'tst.pvd')


if __name__ == '__main__':
    main()
