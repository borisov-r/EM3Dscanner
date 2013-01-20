for z in range(2):
    for y in range(3):
        for x in range(3):
            # y is odd
            if y & 1:
                #y1 = 2 - y
                print "odd: ", x, y, z
            else:
                print "even: ", x, y, z
