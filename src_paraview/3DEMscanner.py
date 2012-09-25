import logging

class :
    def __init__(self, int minXcells, int minYcells, int minZcells,
                       int maxXcells, int maxYcells, int maxZcells):
        logging.basicConfig(filename='ObjectScanClass.log', format='%(levelname)s:%(message)s', filemode='w', level=logging.INFO)
        logging.info('Start')
        wave = Wavelet()
        logging.info('Wavelet generated')
        WholeExtent = self.wave.WholeExtent.GetData()
        logging.info(self.WholeExtent)
        self.wave.WholeExtent.SetData([minXcells, maxXcells, minYcells, maxYcells, minZcells, minZcells])


if __name__ == '__main__':
    # self testing
