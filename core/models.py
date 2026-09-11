from django.db import models
from django.contrib.auth.models import User
from .timerange import TimeRange


# This is consistent with date.weekday()
WEEKDAY = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

RESERVATION_STATUS = (
    (0, 'Booked'),
    (1, 'Arrived'),
)

DEFAULT_RESERVATION_DURATION = 120


class Reservation(models.Model):
    """
    A customer reservation
    """
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservations'
    )
    date = models.DateField()
    # A naive Python time representing local time
    time = models.TimeField()
    # Duration in minutes
    duration = models.IntegerField(default=DEFAULT_RESERVATION_DURATION)
    guest_count = models.IntegerField()
    status = models.IntegerField(choices=RESERVATION_STATUS, default=0)

    class Meta:
        ordering = ['date', 'time', '-guest_count']

    def __str__(self):
        return f"Reservation {self.date} {self.time} by {self.customer}"


class Table(models.Model):
    """
    A table in the restaurant
    """
    table_number = models.IntegerField(unique=True)
    cover_count = models.IntegerField()

    class Meta:
        ordering = ['table_number']

    def __str__(self):
        return f"Table {self.table_number} ({self.cover_count} covers)"


class ServiceTime(models.Model):
    """
    Opening hours for a single service
    """
    weekday = models.IntegerField(choices=WEEKDAY, default=0)
    # A naive Python time representing local time
    start_time = models.TimeField()
    # A naive Python time representing local time
    end_time = models.TimeField()

    def as_range(self):
        return TimeRange(self.start_time, self.end_time)

    class Meta:
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{WEEKDAY[self.weekday][1]} {self.as_range()}"


class ServiceException(models.Model):
    """
    An exception to opening hours for a given date
    """
    date = models.DateField()
    # Is the restaurant open on this date?
    open = models.BooleanField()
    # If self.open, a naive Python time representing local time
    start_time = models.TimeField(default='00:00')
    # If self.open, a naive Python time representing local time
    end_time = models.TimeField(default='00:00')

    def as_range(self):
        return TimeRange(self.start_time, self.end_time)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.date} {self.format_range()}"
