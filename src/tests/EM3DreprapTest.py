import unittest


def AbsoluteValue(n1, n2):
    print abs(n1) + abs(n2)
    return abs(n1) + abs(n2)


class TestPointsToMeasure(unittest.TestCase):
    """ Check if calculated measurement points are correct.
    """
    def testAbsoluteValue(self):
        self.failUnless(AbsoluteValue(-50, 30))


def main():
    unittest.main()

if __name__ == "__main__":
    main()
