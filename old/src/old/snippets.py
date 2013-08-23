from paraview import simple
from paraview import servermanager
from paraview import vtk


class Wave:
    def startUp(self, wavelet):
        self.Data = servermanager.Fetch(wavelet)
        self.ScalarData = self.Data.GetPointData().GetScalars()
        for i in range(int(self.Data.GetNumberOfPoints())):
            self.ScalarData.SetComponent(i, 0, 0.0)
        wavelet.UpdatePipeline()
        for i in range(int(self.Data.GetNumberOfPoints())):
            print("component", i, ":", self.ScalarData.GetComponent(i, 0))
        return wavelet


def main():
    w = servermanager.sources.Wavelet()
    www = Wave()
    pp = www.startUp(w)
    # view = servermanager.CreateRenderView()
    # servermanager.CreateRepresentation(pp, view)
    # Show()
    # RenameSource('MeasuredData')
    # Render()

if __name__ == "__main__":
    main()
