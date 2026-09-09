from datetime import date, timedelta
from itertools import groupby
from django.shortcuts import render
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

    def pad_week(days):
        """
        Given a list of consecutive days all in the same week,
        pad it out so it runs from Monday to Sunday
        """
        days = list(days)
        first = days[0]["date"]
        padded = [{"date": first + timedelta(days=index), "hide": True}
                  for index in range(-first.weekday(), 0)]
        padded += days
        last = days[len(days)-1]["date"]
        padded += [{"date": last + timedelta(days=index+1), "hide": True}
                   for index in range(6 - last.weekday())]
        return padded

    def month_to_weeks(days_in_month):
        """
        Given a number of days in a single month group them by week
        """
        # Group days by week number
        weeks = groupby(days_in_month, lambda x: x["date"].isocalendar().week)
        # And put them in a list
        weeks = [pad_week(days) for k, days in weeks]
        return weeks

    days = get_opening_hours(date.today(), BOOK_AHEAD_DAY_COUNT)

    # Group the days by month
    months = groupby(days, lambda x: x["date"].strftime("%B %Y"))

    months = [{"month": k, "weeks": month_to_weeks(days)}
              for k, days in months]

    return render(
        request,
        'core/reservations.html',
        {
            "months": months
        }
    )
