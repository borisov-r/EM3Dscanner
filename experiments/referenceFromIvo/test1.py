class Point(object):
    def __init__(self, id_, amp, pha):
        self.amp = float(amp)
        self.pha = float(pha)
        self.id_ = int(id_)
    
    def __repr__(self):
        return "Point(id=%d): Amp(%f), Pha(%f)" % (self.id_, self.amp, self.pha)

data = []
for x in range(10):
    data.append([])
    for y in range(10):
        data[-1].append([])
        for z in range(10):
            data[-1][-1].append(Point(0, 0.0, 0.0))


#print data

print data[0][0][0]
data[0][0][0].amp = 12.0
print data[0][0][0]
print data[0][0][1]

with open("test.txt", "w+") as cout:
    for x, xi in enumerate(data):
        for y, yi in enumerate(xi):
            for z, elem in enumerate(yi):
                print >>cout, x,y,z, elem