from datetime import time


def format_time(t):
    return f"{t:%H:%M}"


class TimeRange:
    """
    A time range of less than 24 hours representing a period of service.
    If end_time < start_time it ends at or crosses midnight.
    """
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def slots(self):
        '''
        Generate slots that cover whole hours and the service period.
        A slot is a quarter of an hour.
        '''
        if self.start_time == self.end_time:
            return []

        # Do the calculations in minutes since midnight
        MINS_PER_SLOT = 15
        MINS_PER_HOUR = 60
        MINS_PER_DAY = 24 * MINS_PER_HOUR

        start_mins = self.start_time.hour * MINS_PER_HOUR
        end_mins = (
            self.end_time.hour +
            (self.end_time.minute + MINS_PER_HOUR - 1) // MINS_PER_HOUR
        ) * MINS_PER_HOUR

        # Account for closing times in the wee hours
        if end_mins <= start_mins:
            end_mins += MINS_PER_DAY

        return [time(m % MINS_PER_DAY // MINS_PER_HOUR, m % MINS_PER_HOUR, 0)
                for m in range(start_mins, end_mins, MINS_PER_SLOT)]

    def contains(self, t):
        """Does time t lie within this time range?"""
        if self.start_time == self.end_time:
            return False
        if self.start_time <= t:
            return t < self.end_time or self.end_time < self.start_time
        else:
            return t < self.end_time and self.end_time < self.start_time

    def __str__(self):
        return f"{format_time(self.start_time)} to " \
                f"{format_time(self.end_time)}"
