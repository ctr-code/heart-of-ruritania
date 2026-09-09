from datetime import date, timedelta
from itertools import groupby
from django.shortcuts import render
from .models import ServiceTime, ServiceException


def index(request):
    return render(
        request,
        "core/index.html",
    )


def get_opening_hours(start_date, day_count):
    """
    Integrate the regular service times and the exceptions to
    get a list of opening slots for the given date range
    """

    end_date = start_date + timedelta(days=day_count)

    service_times = ServiceTime.objects.order_by('weekday')

    # Group the service times by weekday
    service_groups = groupby(service_times, lambda x: x.weekday)
    # Create a map from weekday to service times on that day
    service_map = {k: list(group) for k, group in service_groups}

    exceptions = ServiceException.objects.filter(
        date__gte=start_date, date__lt=end_date
    ).order_by('date')

    # Group the exceptions by date
    exception_groups = groupby(exceptions, lambda x: x.date)
    # Create a map from date to exceptions on that date
    exception_map = {k: list(group) for k, group in exception_groups}

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
    def format_day(day):
        return {
            "date": f"{day["date"]:%a %d %b}",
            "ranges": [t.format_range()
                       for t in day["times"]] if day["open"] else ["CLOSED"],
        }

    days = get_opening_hours(date.today(), 14)
    days = [format_day(day) for day in days]

    return render(
        request,
        "core/hours.html",
        {
            "days": days
        }
    )
