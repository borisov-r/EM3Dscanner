###########################################################################
#
# Here will be placed main source of the project (the logic of the scanner)
#
# for now the script should be started in paraveiw's python interpretator
#
# Author: Radoslav Borisov
# Date: 17.09.2012
# License: GPL 3.0
#
###########################################################################

from paraview import vtk

# if wavelet is created in paraview and applied
#wave = GetActiveSource()
#data = servermanager.Fetch(wave)
#scalars = data.GetPointData().GetScalars()
#scalars.SetName('Amplitude')

# else create wavelet manually in python
wave = Wavelet()
wave.WholeExtent.GetData()  # returns values for X, Y, Z direction coords
                            # [-10, 10, -10, 10, -10, 10]
# sets number of cells to be measured 100 x 100 x 10 = 100000 cells
wave.WholeExtent.SetData([0,100,0,100,0,10])

Show()
Render()

data = servermanager.Fetch(wave)
# show number of cells - returns: '100000L'
data.GetNumberOfCells()
# show number of points - returns: '112211L'
data.GetNumberOfPoints()

# working with scalar data
scalar = data.GetPointData().GetScalars()
print scalar.GetNumberOfComponents()            # returns: '1'
print scalar.GetNumberOfTuples()                # returns: '112211'
scalar.SetComponent(0, 10, 0.0)                 # sets in array 0, component 10 to 0.0
scalar.GetComponent(0, 10)                      # returns the value of the 10 component in 0 array

scalar.GetName()                                # returns: 'RTdata'
scalar.SetName('Amplitude')                     # returns: '' - sets the name of the scalars to 'Amplitude'
scalar.GetName()                                # returns: 'Amplitude'

data.GetScalarType()                            # returns: '11'
data.SetScalarType()                            # returns: '' - sets Scalar to given type


/*
points = scalars.GetNumberOfTuples()
>>> points
8L
>>> print points
8
>>> for i in range(scalars.GetNumberOfTuples()):
    ...     scalars.SetComponent(0, i, 0.0)
    ...
    >>> for i in range(scalars.GetNumberOfTuples()):
        ...     print scalars.GetComponent(0, i)
        ...
        0.0
        0.0
        0.0
        0.0
        0.0
        0.0
        0.0
        0.0
        >>> Render()
*/
