from django.db import models
from django.core.validators import MinValueValidator
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
SHORTEST_RESERVATION_DURATION = 90


class Reservation(models.Model):
    """
    A customer reservation
    """
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservations'
    )
    # The date on which the service started.  If the reservation is after
    # midnight the reservation will fall on the next day.
    svc_date = models.DateField()

    # TODO: Add the actual reservation date
    # A naive Python time representing the local time of the reservation
    time = models.TimeField()

    # Duration in minutes
    duration = models.PositiveIntegerField(
        default=DEFAULT_RESERVATION_DURATION)

    guest_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])

    status = models.PositiveIntegerField(
        choices=RESERVATION_STATUS, default=0)

    class Meta:
        ordering = ['svc_date', 'time', '-guest_count']

    def __str__(self):
        return f"Reservation {self.svc_date} {self.time} by {self.customer}"


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

    class Meta:
        ordering = ['weekday', 'start_time']

    def as_range(self):
        return TimeRange(self.start_time, self.end_time)

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

    class Meta:
        ordering = ['date', 'start_time']

    def as_range(self):
        return TimeRange(self.start_time, self.end_time)

    def __str__(self):
        return f"{self.date} {self.as_range()}"
