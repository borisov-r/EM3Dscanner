import datetime

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(0, 7)

class YearPattern:

    def __init__(self, year):
        self.year = year

    def matches(self, date):
        return self.year == date.year

class MonthPattern:

    def __init__(self, month):
        self.month = month

    def matches(self, date):
        return self.month == date.month

class DayPattern:

    def __init__(self, day):
        self.day = day

    def matches(self, date):
        return self.day == date.day

class WeekdayPattern:

    def __init__(self, weekday):
        self.weekday = weekday

    def matches(self, date):
        return self.weekday == date.weekday()

class NthWeekdayInMonthPattern:

    def __init__(self, n, weekday):
        self.n = n
        self.weekday = weekday

    def matches(self, date):
        if self.weekday != date.weekday():
            return False
        return self.n == self.getWeekdayNumber(date)

    def getWeekdayNumber(self, date):
        n = 1
        while True:
            previousDate = date - datetime.timedelta(7 * n);
            if previousDate.month == date.month:
                n += 1
            else:
                break
        return n

class LastWeekdayInMonthPattern:

    def __init__(self, weekday):
        self.weekday = weekday

    def matches(self, date):
        nextWeek = date + datetime.timedelta(7)
        return self.weekday == date.weekday() and nextWeek.month != date.month

class LastDayInMonthPattern:

    def matches(self, date):
        tomorrow = date + datetime.timedelta(1)
        return tomorrow.month != date.month

class CompositePattern:

    def __init__(self):
        self.patterns = []

    def add(self, pattern):
        self.patterns.append(pattern)

    def matches(self, date):
        for pattern in self.patterns:
            if not pattern.matches(date):
                return False
        return True
