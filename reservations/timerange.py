from datetime import time


def format_time(t):
    return f"{t:%H:%M}"


class Slot:
    """
    A slot is a value type representing a quarter of an hour period.
    Slots are indexed from midnight on the start day of a time range.
    When a time range extends past midnight, a slot index may reflect
    a time greater than 24 hours.
    """
    MINS_PER_HOUR = 60
    HOURS_PER_DAY = 24
    MINS_PER_DAY = HOURS_PER_DAY * MINS_PER_HOUR
    MINS_PER_SLOT = 15
    SLOTS_PER_HOUR = MINS_PER_HOUR // MINS_PER_SLOT
    SLOTS_PER_DAY = HOURS_PER_DAY * SLOTS_PER_HOUR

    @classmethod
    def from_starttime(cls, time, after_midnight=False):
        """
        Create a Slot representing the start of a time range.

        :param time: The start time of a time range.
        :param after_midnight: Does the time represent a time after midnight?
        """
        minutes = time.hour * Slot.MINS_PER_HOUR + time.minute
        if after_midnight:
            minutes += Slot.MINS_PER_DAY
        return Slot(minutes // Slot.MINS_PER_SLOT)

    @classmethod
    def from_longtime(cls, long_hour, minute):
        """
        Create a Slot containing the given time.

        :param long_hour: The time in hours measured from midnight on the start
        day of the time range so it may be more than 23.
        :param minute: The time in minutes (0-59).
        """
        if long_hour < 0 or long_hour >= 2 * Slot.HOURS_PER_DAY or \
                minute < 0 or minute >= Slot.MINS_PER_HOUR:
            raise ValueError()
        minutes = long_hour * Slot.MINS_PER_HOUR + minute
        return Slot(minutes // Slot.MINS_PER_SLOT)

    @classmethod
    def from_endtime(cls, time, after_midnight):
        """
        Create a Slot representing the end of a time range.

        :param time: The end time of a time range.
        :param after_midnight: Does the time represent a time after midnight?
        """
        minutes = time.hour * Slot.MINS_PER_HOUR + time.minute
        if after_midnight:
            minutes += Slot.MINS_PER_DAY
        index = minutes // Slot.MINS_PER_SLOT
        if minutes % Slot.MINS_PER_SLOT != 0:
            index += 1
        return Slot(index)

    def __init__(self, index):
        self.index = index

    def __eq__(self, other):
        return self.index == other.index

    def __ne__(self, other):
        return self.index != other.index

    def __hash__(self):
        return self.index.__hash__()

    def hour(self):
        """Return the hour part of the slot considered as a time"""
        return (self.index % Slot.SLOTS_PER_DAY) // Slot.SLOTS_PER_HOUR

    def minute(self):
        """Return the minute part of the slot considered as a time"""
        return (self.index % Slot.SLOTS_PER_HOUR) * Slot.MINS_PER_SLOT

    def long_hour(self):
        """Return the hour part of the slot possibly extended past midnight"""
        return self.index // Slot.SLOTS_PER_HOUR

    def as_time(self):
        return time(self.hour(), self.minute())

    def __str__(self):
        return f"{self.hour():02}:{self.minute():02}"


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

    @classmethod
    def from_time_duration(cls, start_time, duration):
        """
        Create a TimeRange from a start time and a duration in minutes

        :param start_time: A datetime.time representing the start of the
        period.
        :param duration: The duration of the period in minutes.
        """
        # The start time of the period in minutes since midnight
        start_mins = start_time.hour * Slot.MINS_PER_HOUR + start_time.minute
        # The end time of the period in minutes since midnight
        end_mins = (start_mins + duration) % Slot.MINS_PER_DAY
        # The end time as a datetime.time
        end_time = time(end_mins // Slot.MINS_PER_HOUR,
                        end_mins % Slot.MINS_PER_HOUR)
        # Construct and return the corresponding TimeRange
        return TimeRange(start_time, end_time)

    def round_to_hours(self):
        """
        Return a pair of slots representing this time range rounded to hours.
        """
        return (self.start_slot.index -
                (self.start_slot.index % Slot.SLOTS_PER_HOUR),
                ((self.end_slot.index + Slot.SLOTS_PER_HOUR - 1)
                 // Slot.SLOTS_PER_HOUR) * Slot.SLOTS_PER_HOUR)

    def slots(self):
        """
        Return a list of slots that cover this time range.
        """
        if self.start_time == self.end_time:
            return []

        return [Slot(index)
                for index in range(self.start_slot.index, self.end_slot.index)]

    def extended_slots(self):
        """
        Return a list of slots that cover this time range extended to whole
        hours.
        """
        if self.start_time == self.end_time:
            return []

        (start, end) = self.round_to_hours()

        return [Slot(index) for index in range(start, end)]

    def slot_from_time(self, t):
        """Get the slot in this time range containing the time t, if any"""
        if self.start_time == self.end_time:
            return False
        slot = Slot.from_starttime(t, self.start_time > t)
        if slot.index >= self.end_slot.index:
            return None
        return slot

    def remaining(self, slot):
        """
        Given a slot within this time range, return the remaining minutes
        before the end of the time range.
        """
        return (self.end_slot.index - slot.index) * Slot.MINS_PER_SLOT

    def contains_slot(self, slot):
        """Does this time range contain the given slot?"""
        return self.start_slot.index <= slot.index and \
            slot.index < self.end_slot.index

    def __str__(self):
        return f"{format_time(self.start_time)} to " \
                f"{format_time(self.end_time)}"
