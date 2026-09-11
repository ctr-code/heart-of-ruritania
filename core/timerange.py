from datetime import time


def format_time(t):
    return f"{t:%H:%M}"


class Slot:
    """
    A slot is a quarter of an hour period.  Slots are indexed from midnight.
    """
    MINS_PER_HOUR = 60
    MINS_PER_DAY = 24 * MINS_PER_HOUR
    MINS_PER_SLOT = 15
    SLOTS_PER_HOUR = MINS_PER_HOUR // MINS_PER_SLOT

    @classmethod
    def from_starttime(cls, time):
        minutes = time.hour * Slot.MINS_PER_HOUR + time.minute
        return Slot(minutes // Slot.MINS_PER_SLOT)

    @classmethod
    def from_endtime(cls, time, after_midnight):
        minutes = time.hour * Slot.MINS_PER_HOUR + time.minute
        if after_midnight:
            minutes += Slot.MINS_PER_DAY
        index = minutes // Slot.MINS_PER_SLOT
        if minutes % Slot.MINS_PER_SLOT != 0:
            index += 1
        return Slot(index)

    def __init__(self, index):
        self.index = index

    def round_down_to_hour(self):
        return 0


class TimeRange:
    """
    A time range of less than 24 hours representing a period of service.
    If end_time < start_time the range ends at or crosses midnight.
    """

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.start_slot = Slot.from_starttime(start_time)
        self.end_slot = Slot.from_endtime(end_time, end_time < start_time)

    def slots(self):
        '''
        Generate slots that cover whole hours and the service period.
        A slot is a quarter of an hour.
        '''
        if self.start_time == self.end_time:
            return []

        # Round the start_time and end_time to whole hours
        start_mins = self.start_time.hour * Slot.MINS_PER_HOUR
        end_mins = (
            self.end_time.hour +
            (self.end_time.minute + Slot.MINS_PER_HOUR - 1)
            // Slot.MINS_PER_HOUR
        ) * Slot.MINS_PER_HOUR

        # Account for closing times in the wee hours
        if end_mins <= start_mins:
            end_mins += Slot.MINS_PER_DAY

        return [time(m % Slot.MINS_PER_DAY // Slot.MINS_PER_HOUR,
                     m % Slot.MINS_PER_HOUR, 0)
                for m in range(start_mins, end_mins, Slot.MINS_PER_SLOT)]

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
