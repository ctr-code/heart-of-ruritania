from datetime import date, timedelta
from itertools import groupby
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ServiceTime, ServiceException


OPENING_HOURS_DAY_COUNT = 14
BOOK_AHEAD_DAY_COUNT = 60


def index(request):
    return render(
        request,
        "core/index.html",
    )


def map_by_key(items, key):
    """
    Return a map from a key value to a list of items with that key

    :param items: Elements to divide into groups according to the key function
    :param key: A function for computing the group category of an item
    """
    return {k: list(group) for k, group in groupby(items, key)}


def valid_booking_period():
    """Return the range of time in which bookings are valid"""
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=BOOK_AHEAD_DAY_COUNT)
    return (start_date, end_date)


def get_opening_hours(start_date, day_count):
    """
    Integrate the regular service times and the exceptions to
    get a list of opening slots for the given date range
    """

    end_date = start_date + timedelta(days=day_count)

    service_times = ServiceTime.objects.order_by('weekday')

    # Create a map from weekday to service times on that day
    service_map = map_by_key(service_times, lambda x: x.weekday)

    exceptions = ServiceException.objects.filter(
        date__gte=start_date, date__lt=end_date
    ).order_by('date')

    # Create a map from date to exceptions on that date
    exception_map = map_by_key(exceptions, lambda x: x.date)

    result = []

    for index in range(day_count):
        date = start_date + timedelta(days=index)
        times = exception_map.get(date)

        if times is None:
            # Use the regular service times
            times = service_map.get(date.weekday())
        elif not times[0].open:
            times = None

        if times is None:
            result.append({"date": date, "open": False})
        else:
            result.append({"date": date, "open": True, "times": times})

    return result


def opening_hours(request):
    """
    View for the opening hours page
    """
    def format_day(day):
        return {
            # Note that '%-d' is glibc only, i.e. not windows
            "date": f"{day["date"]:%a %-d %b}",
            "ranges": [t.format_range()
                       for t in day["times"]] if day["open"] else ["CLOSED"],
        }

    days = get_opening_hours(date.today(), OPENING_HOURS_DAY_COUNT)
    days = [format_day(day) for day in days]

    return render(
        request,
        "core/hours.html",
        {
            "days": days
        }
    )


@login_required
def reservations(request):
    """
    View for the reservations page
    """

    def date_month(day):
        """Return the month associated with a day"""
        return date(day.year, day.month, 1)

    def next_month(day):
        """Return the next month after the given date"""
        return date_month(date_month(day) + timedelta(days=31))

    def calendar(month, start_date, end_date):
        """
        Return a list of dates within the given month and the given date range,
        extended to run from a Monday to a Sunday
        """
        # Clamp the view of the month within start_date and end_date
        start_date = max(month, start_date)
        end_date = min(next_month(month), end_date)

        # Extend the range so it runs from a Monday to a Monday
        start_date = start_date + timedelta(days=-start_date.weekday())
        end_date = end_date + timedelta(days=(7 - end_date.weekday()) % 7)

        # Return the list of days; always a whole number of weeks
        return [start_date + timedelta(days=index)
                for index in range((end_date-start_date).days)]

    # Get the date range of the booking period
    (start_date, end_date) = valid_booking_period()

    # Get the days on which the restaurant is open
    days = get_opening_hours(start_date, BOOK_AHEAD_DAY_COUNT)
    open_days = set(d["date"] for d in days if d["open"])

    # Construct the months
    month = date_month(start_date)
    end_month = next_month(end_date + timedelta(days=-1))
    months = []
    while month < end_month:
        cal = [
            {
                "date": d,
                "open": d in open_days,
                "off":
                    d < start_date or d >= end_date or d.month != month.month,
            }
            for d in calendar(month, start_date, end_date)
        ]
        months.append(
            {
                "month": month,
                "name": month.strftime("%B %Y"),
                "days": cal,
            }
        )
        month = next_month(month)

    # And render
    return render(
        request,
        'core/reservations.html',
        {
            "months": months
        }
    )


def reservation_times(request, year, month, day):
    try:
        reservation_date = date(year, month, day)
    except ValueError:
        # If the date is bogus return to the reservations page
        return HttpResponseRedirect(reverse('reservations'))

    # Get the date range of the booking period
    (start_date, end_date) = valid_booking_period()

    # If the date is outside the booking period return to the reservations page
    if reservation_date < start_date or reservation_date >= end_date:
        return HttpResponseRedirect(reverse('reservations'))

    details = get_opening_hours(reservation_date, 1)[0]
    if not details["open"]:
        # If not open on this date return to the reservations page
        return HttpResponseRedirect(reverse('reservations'))

    return render(
        request,
        'core/reservation_times.html',
        {
            "date": reservation_date
        }
    )
