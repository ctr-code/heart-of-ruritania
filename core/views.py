from datetime import date, time, timedelta
from itertools import groupby
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reservation, ServiceTime, ServiceException, Table
from .timerange import format_time, Slot, TimeRange

# The number of days displayed on the opening hours page
OPENING_HOURS_DAY_COUNT = 14
# A reservation can be made for this many days in the future
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
    """Return the range of dates in which reservations may be made"""
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=BOOK_AHEAD_DAY_COUNT)
    return (start_date, end_date)


def validate_reservation_date(year, month, day):
    """
    Check that the given date is valid for a reservation.
    Return the date and the service details for that date.
    """

    # This may throw a ValueError, which will be caught by the caller
    reservation_date = date(year, month, day)

    # Get the date range of the booking period
    (start_date, end_date) = valid_booking_period()

    # If the date is outside the booking period throw an error
    if reservation_date < start_date or reservation_date >= end_date:
        raise ValueError()

    details = get_opening_hours(reservation_date, 1)[0]
    if not details["open"]:
        # If restaurant not open on this date throw an error
        raise ValueError()

    return (reservation_date, details)


def get_opening_hours(start_date, day_count):
    """
    Integrate the regular service times and the exceptions to
    get a list of opening slots for the given date range
    """

    end_date = start_date + timedelta(days=day_count)

    service_times = ServiceTime.objects.order_by('weekday', 'start_time')

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
            times = [TimeRange(t.start_time, t.end_time) for t in times]
            result.append({"date": date, "open": True, "times": times})

    return result


def allocate_reservations_to_tables(service, reservations):
    """
    Update each reservation with a free table
    """

    # Do calculations in minutes since midnight
    def minutes_since_midnight(time):
        return time.hour * Slot.MINS_PER_HOUR + time.minute

    # Sort tables to ensure smaller tables are preferred
    tables = Table.objects.order_by('cover_count')
    for table in tables:
        table.open_from = 0

    service_start = minutes_since_midnight(service.start_time)

    for reservation in reservations:
        reservation.table = None
        if service.contains(reservation.time):
            start_time = minutes_since_midnight(reservation.time)
            # Account for start times after midnight
            if start_time < service_start:
                start_time += Slot.MINS_PER_DAY
            for table in tables:
                if table.cover_count >= reservation.guest_count and \
                        start_time >= table.open_from:
                    reservation.table = table
                    # Note that this can go past midnight, and that's fine
                    table.open_from = start_time + reservation.duration
                    break


def slot_availability(service, reservations, slots):
    """
    Update each slot with the largest number of guests that can be
    accommodated at that time.
    """
    # For each slot calculate the largest remaining table.
    # Then take the minimum over the next DEFAULT_RESERVATION_DURATION.
    allocate_reservations_to_tables(service, reservations)
    # Give each slot a set of all the tables
    slot_map = {slot["time"]: slot for slot in slots}
    for slot in slots:
        slot["tables"] = set(Table.objects.all())
    for reservation in reservations:
        if reservation.table:
            slot_count = (reservation.duration + Slot.MINS_PER_SLOT - 1) \
                // Slot.MINS_PER_SLOT * Slot.MINS_PER_SLOT
            pass

    print(slots)
    return slots


def opening_hours(request):
    """
    View for the opening hours page
    """
    def format_day(day):
        return {
            # Note that '%-d' is glibc only, i.e. not windows
            "date": f"{day["date"]:%a %-d %b}",
            "ranges": day["times"] if day["open"] else ["CLOSED"],
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
            "reservations": request.user.reservations.all(),
            "months": months
        }
    )


@login_required
def reservation_times(request, year, month, day):
    try:
        (reservation_date, details) = \
            validate_reservation_date(year, month, day)
    except ValueError:
        # If the date is bogus return to the reservations page
        return HttpResponseRedirect(reverse('reservations'))

    services = details["times"]

    reservations = Reservation.objects.filter(date=reservation_date)

    services_plus = [
        {
            "name": service,
            "slots": slot_availability(service, reservations,
                [
                    {
                        "time": t,
                        "name": format_time(t),
                        "open": service.contains(t),
                    }
                    for t in service.slots()
                ]
            ),
        }
        for service in services
    ]

    return render(
        request,
        'core/reservation_times.html',
        {
            "date": reservation_date,
            "services": services_plus,
        }
    )


@login_required
def reserve(request, year, month, day, hour, minute):
    if request.method == "POST":
        try:
            (reservation_date, details) = \
                validate_reservation_date(year, month, day)
            reservation_time = time(hour, minute)
        except ValueError:
            # If the date or time is bogus return to the reservations page
            return HttpResponseRedirect(reverse('reservations'))

        # The services containing the time (should be exactly one)
        services = [s
                    for s in details["times"] if s.contains(reservation_time)]
        if len(services) == 0:
            # If the time lies outwith the service hours return to reservations
            return HttpResponseRedirect(reverse('reservations'))

        reservation = Reservation()
        reservation.customer = request.user
        reservation.date = reservation_date
        reservation.time = reservation_time
        # TODO: reservation.duration
        # TODO: How does this get entered?!!!
        reservation.guest_count = 4
        reservation.save()

        messages.add_message(
            request, messages.ERROR,
            f'Reservation complete! {reservation}'
        )
    return HttpResponseRedirect(reverse('reservations'))
