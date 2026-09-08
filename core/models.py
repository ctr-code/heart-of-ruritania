from django.db import models
from django.contrib.auth.models import User


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


def format_time(t):
    return f"{t:%H:%M}"


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
    guest_count = models.IntegerField()
    status = models.IntegerField(choices=RESERVATION_STATUS, default=0)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"Reservation {self.date} {self.time} by {self.customer}"


class Table(models.Model):
    """
    A table in the restaurant
    """
    table_number = models.IntegerField()
    cover_count = models.IntegerField()

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

    def __str__(self):
        return f"{WEEKDAY[self.weekday][1]} " \
               f"{format_time(self.start_time)} to " \
               f"{format_time(self.end_time)}"


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

    def __str__(self):
        if self.open:
            return f"{self.date} " \
                   f"{format_time(self.start_time)} to " \
                   f"{format_time(self.end_time)}"
        else:
            return f"{self.date} CLOSED"
