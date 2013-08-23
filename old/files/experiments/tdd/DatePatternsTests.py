import datetime
import unittest

from DatePatterns import *


class YearPatternTests(unittest.TestCase):

    def setUp(self):
        self.d = datetime.date(2004, 9, 29)

    def testMatches(self):
        yp = YearPattern(2004)
        self.failUnless(yp.matches(self.d))

    def testNotMatches(self):
        yp = YearPattern(2003)
        self.failIf(yp.matches(self.d))


class MonthPatternTests(unittest.TestCase):

    def setUp(self):
        self.d = datetime.date(2004, 9, 29)

    def testMatches(self):
        mp = MonthPattern(9)
        self.failUnless(mp.matches(self.d))

    def testNotMatches(self):
        mp = MonthPattern(8)
        self.failIf(mp.matches(self.d))


class DayPatternTests(unittest.TestCase):

    def setUp(self):
        self.d = datetime.date(2004, 9, 29)

    def testMatches(self):
        dp = DayPattern(29)
        self.failUnless(dp.matches(self.d))

    def testNotMatches(self):
        dp = DayPattern(28)
        self.failIf(dp.matches(self.d))


class WeekdayPatternTests(unittest.TestCase):

    def setUp(self):
        self.d = datetime.date(2004, 9, 29)

    def testMatches(self):
        wp = WeekdayPattern(WEDNESDAY)
        self.failUnless(wp.matches(self.d))

    def testNotMatches(self):
        wp = WeekdayPattern(TUESDAY)
        self.failIf(wp.matches(self.d))


class CompositePatternTests(unittest.TestCase):

    def setUp(self):
        self.d = datetime.date(2004, 9, 29)

    def testMatches(self):
        cp = CompositePattern()
        cp.add(YearPattern(2004))
        cp.add(MonthPattern(9))
        cp.add(DayPattern(29))
        self.failUnless(cp.matches(self.d))

    def testNotMatches(self):
        cp = CompositePattern()
        cp.add(YearPattern(2004))
        cp.add(MonthPattern(9))
        cp.add(DayPattern(28))
        self.failIf(cp.matches(self.d))

    def testMatchesWithoutYear(self):
        cp = CompositePattern()
        cp.add(MonthPattern(9))
        cp.add(DayPattern(29))
        self.failUnless(cp.matches(self.d))


class NthWeekdayInMonthPatternTests(unittest.TestCase):

    def setUp(self):
        self.pattern = NthWeekdayInMonthPattern(1, WEDNESDAY)

    def testMatches(self):
        firstWedOfSep2004 = datetime.date(2004, 9, 1)
        self.failUnless(self.pattern.matches(firstWedOfSep2004))

    def testNotMatches(self):
        secondWedOfSep2004 = datetime.date(2004, 9, 8)
        self.failIf(self.pattern.matches(secondWedOfSep2004))


class LastWeekdayInMonthPatternTests(unittest.TestCase):

    def setUp(self):
        self.pattern = LastWeekdayInMonthPattern(WEDNESDAY)

    def testMatches(self):
        lastWedOfSep2004 = datetime.date(2004, 9, 29)
        self.failUnless(self.pattern.matches(lastWedOfSep2004))

    def testNotMatches(self):
        firstWedOfSep2004 = datetime.date(2004, 9, 1)
        self.failIf(self.pattern.matches(firstWedOfSep2004))


class LastDayInMonthPatternTests(unittest.TestCase):

    def setUp(self):
        self.pattern = LastDayInMonthPattern()

    def testMatches(self):
        lastDayInSep2004 = datetime.date(2004, 9, 30)
        self.failUnless(self.pattern.matches(lastDayInSep2004))

    def testNotMatches(self):
        secondToLastDayInSep2004 = datetime.date(2004, 9, 29)
        self.failIf(self.pattern.matches(secondToLastDayInSep2004))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
