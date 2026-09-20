from datetime import date, timedelta
from itertools import groupby
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from .models import Reservation, ServiceTime, ServiceException, Table, \
    DEFAULT_RESERVATION_DURATION, SHORTEST_RESERVATION_DURATION
from .timerange import Slot, TimeRange

# The number of days displayed on the opening hours page
OPENING_HOURS_DAY_COUNT = 14
# A reservation can be made for this many days in the future
BOOK_AHEAD_DAY_COUNT = 60


def map_by_key(items, key):
    """
    Return a map from a key value to a list of items with that key

    :param items: Elements to divide into groups according to the key function
    :param key: A function for computing the group category of an item
    """
    return {k: list(group) for k, group in groupby(items, key)}


def valid_booking_period(admin_view):
    """
    Return the range of dates in which reservations may be made.
    Additionally, include today if admin_view.
    """
    start_date = date.today()
    end_date = start_date + timedelta(days=BOOK_AHEAD_DAY_COUNT + 1)
    if not admin_view:
        start_date += timedelta(days=1)
    return (start_date, end_date)


def validate_reservation_date(year, month, day):
    """
    Check that the given date is valid for a reservation.
    Return the date and the service details for that date.
    """

    # This may throw a ValueError, which will be caught by the caller
    reservation_date = date(year, month, day)

    # Get the date range of the booking period
    (start_date, end_date) = valid_booking_period(False)

    # If the date is outside the booking period throw an error
    if reservation_date < start_date or reservation_date >= end_date:
        raise ValueError()

    opening_hours = get_opening_hours(reservation_date, 1)[0]
    if not opening_hours["open"]:
        # If restaurant not open on this date throw an error
        raise ValueError()

    return (reservation_date, opening_hours)


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

    def duration_in_slots(reservation):
        range = TimeRange.from_time_duration(
            reservation.time, reservation.duration)
        return range.end_slot.index - range.start_slot.index

    # Sort tables to ensure smaller tables are preferred
    tables = Table.objects.order_by('cover_count')
    for table in tables:
        table.open_from = 0

    for reservation in reservations:
        reservation.table = None
        reservation.slot = service.slot_from_time(reservation.time)

    # Reservations can't be ordered by time, because reservations just
    # after midnight would precede earlier ones in the same service.
    # Sort the reservations by slot.
    sorted = [reservation for reservation in reservations if reservation.slot]
    sorted.sort(key=lambda r: r.slot.index)

    for reservation in sorted:
        reservation.slot_count = duration_in_slots(reservation)
        for table in tables:
            if table.cover_count >= reservation.guest_count and \
                    reservation.slot.index >= table.open_from:
                reservation.table = table
                # Note that this can go past midnight, and that's fine
                table.open_from = \
                    reservation.slot.index + reservation.slot_count
                break


def slot_availability(service, reservations, slots):
    """
    Update each slot with the largest number of guests that can be
    accommodated at that time and for the duration of a booking.
    """
    # For each slot calculate the largest remaining table.
    # Then take the minimum over the next DEFAULT_RESERVATION_DURATION.
    allocate_reservations_to_tables(service, reservations)

    slots_offset = slots[0]["slot"].index

    # Give each slot a set of all the tables
    for slot in slots:
        slot["tables"] = set(Table.objects.all())

    # Remove tables from the slots during which they are in use
    for reservation in reservations:
        if reservation.table:
            for slot_index in range(
                reservation.slot.index,
                reservation.slot.index + reservation.slot_count
            ):
                index = slot_index - slots_offset
                if 0 <= index and index < len(slots):
                    slots[index]["tables"].remove(reservation.table)

    # Get the maximum number of covers available in each slot
    for slot in slots:
        max_table = max(slot["tables"], key=lambda t: t.cover_count)
        slot["max"] = max_table.cover_count
        del slot["tables"]

    default_slot_count = DEFAULT_RESERVATION_DURATION // Slot.MINS_PER_SLOT
    shortest_slot_count = SHORTEST_RESERVATION_DURATION // Slot.MINS_PER_SLOT

    # Get the number of slots ignoring rounding slots on the end
    slot_count = len(slots)
    while slot_count > 0 and not slots[slot_count - 1]["open"]:
        slot_count -= 1

    # Calculate the maximum size of a booking in each slot
    for index in range(0, len(slots)):
        remaining = slot_count - index
        slot = slots[index]
        if remaining < shortest_slot_count:
            slot["max"] = 0
            slot["open"] = False
        else:
            check_count = min(remaining, default_slot_count)
            # The maximum size of a booking in this slot is the minimum of the
            # available covers in this and the immediately following slots.
            slot_max = min(slots[i]["max"]
                           for i in range(index, index + check_count))
            slot["max"] = slot_max

    return slots


def calendar_view(request, admin_view):
    """
    Internal function to generate a calendar view for an admin or non-admin.
    Arranging it like this gives the admin access to the non-admin view.
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

    # This should never happen, but just in case
    if admin_view and not request.user.is_staff:
        raise PermissionDenied

    # Get the date range of the booking period
    (start_date, end_date) = valid_booking_period(admin_view)

    # Get the existing reservations
    if admin_view:
        reservations = Reservation.objects
    else:
        reservations = request.user.reservations

    # Filter the reservations to the booking period
    reservations = reservations.filter(
        svc_date__gte=start_date, svc_date__lt=end_date
    )

    reservation_dates = set(r.svc_date for r in reservations)

    # Get the days on which the restaurant is open
    days = get_opening_hours(start_date, (end_date - start_date).days)
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
                "edit": d in open_days and d in reservation_dates
            }
            for d in calendar(month, start_date, end_date)
        ]
        months.append(
            {
                "date": month,
                "name": month.strftime("%B %Y"),
                "days": cal,
            }
        )
        month = next_month(month)

    # And render
    return render(
        request,
        'reservations/reservations.html',
        {
            "months": months,
            "admin_view": admin_view,
            "day_url_name": 'admin_day' if admin_view else 'reservation_times',
        }
    )


def opening_hours(request):
    """
    View for the opening hours page
    """
    def format_day(day):
        return {
            # Note that '%-d' is glibc only, i.e. not windows
            "date": f"{day["date"]:%a %-d %b}",
            "ranges": day["times"] if day["open"] else [""],
        }

    days = get_opening_hours(date.today(), OPENING_HOURS_DAY_COUNT)
    days = [format_day(day) for day in days]

    return render(
        request,
        "reservations/hours.html",
        {
            "days": days
        }
    )


@login_required
def reservations(request):
    """
    View for the customer reservations page where a date can be selected
    """
    return calendar_view(request, False)


@staff_member_required
def admin_calendar(request):
    """
    View for the admin reservations page where a date can be selected
    """
    return calendar_view(request, True)


@login_required
def reservation_times(request, year, month, day):
    """
    View for the reservation_times page where a time can be selected.
    UI for making, editing and deleting reservations.
    """
    try:
        (service_date, opening_hours) = \
            validate_reservation_date(year, month, day)
    except ValueError:
        # If the date is bogus return to the reservations page
        return HttpResponseRedirect(reverse('reservations'))

    services = opening_hours["times"]

    reservations = Reservation.objects.filter(svc_date=service_date)
    user_reservations = reservations.filter(customer=request.user)
    user_reservation_slots = set(r.slot() for r in user_reservations)
    editing = user_reservations.exists()

    reservation = user_reservations[0] if editing else None
    id = reservation.id if editing else None
    guest_count = reservation.guest_count if editing else 0

    # Iterate over the services adding information needed for the UI
    services_plus = [
        {
            "name": service,
            "slots": slot_availability(
                service,
                [r for r in reservations if r != reservation],
                [
                    {
                        "slot": slot,
                        "name": f"{slot}",
                        "open": service.contains_slot(slot),
                        "edit": slot in user_reservation_slots,
                    }
                    for slot in service.slots()
                ]
            ),
        }
        for service in services
    ]

    return render(
        request,
        'reservations/reservation_times.html',
        {
            "date": service_date,
            "slot": user_reservations[0].slot() if editing else None,
            "editing": editing,
            "id": id,
            "guest_count": guest_count,
            "services": services_plus,
        }
    )


@staff_member_required
def admin_day(request, year, month, day):
    """
    The admin's day view.
    """
    try:
        service_date = date(year, month, day)
    except ValueError:
        # If the date is bogus return to the admin_calendar page
        return HttpResponseRedirect(reverse('admin_calendar'))

    reservations = Reservation.objects.filter(svc_date=service_date) \
        .order_by('res_date', 'time', '-guest_count')

    services = get_opening_hours(service_date, 1)[0]["times"]

    # Iterate over the services adding information needed for the UI
    services_plus = [
        {
            "name": service,
            "reservations": [
                r for r in reservations if service.contains_slot(r.slot())
            ],
        }
        for service in services
    ]

    return render(
        request,
        'reservations/admin_day.html',
        {
            "date": service_date,
            "services": services_plus,
        }
    )


@login_required
def reserve(request, year, month, day, long_hour, minute):
    """
    The reserve endpoint, which makes a reservation and redirects to the
    reservations page
    """
    if request.method == "POST":
        try:
            (service_date, opening_hours) = \
                validate_reservation_date(year, month, day)
            reservation_slot = Slot.from_longtime(long_hour, minute)
        except ValueError:
            # If the date or time is bogus return to the reservations page
            return HttpResponseRedirect(reverse('reservations'))

        # The services containing the slot (should be exactly one)
        services = [s for s in opening_hours["times"]
                    if s.contains_slot(reservation_slot)]

        if len(services) == 0:
            # If the time lies outwith the service hours return to reservations
            return HttpResponseRedirect(reverse('reservations'))

        # Check this is a valid time within the service (i.e. not at the end)
        service_remaining = services[0].remaining(reservation_slot)
        duration = min(DEFAULT_RESERVATION_DURATION, service_remaining)
        if duration < SHORTEST_RESERVATION_DURATION:
            return HttpResponseRedirect(reverse('reservations'))

        reservations = Reservation.objects.filter(svc_date=service_date)
        user_reservations = reservations.filter(customer=request.user)
        editing = user_reservations.exists()
        reservation = user_reservations[0] if editing else None

        reservation_form = ReservationForm(
            data=request.POST, instance=reservation)

        if reservation_form.is_valid():
            # TODO: Check a reservation with this guest_count is feasible
            reservation = reservation_form.save(commit=False)

            reservation.customer = request.user
            reservation.svc_date = service_date
            reservation.res_date = service_date + \
                timedelta(days=reservation_slot.long_hour()
                          // Slot.HOURS_PER_DAY)
            reservation.time = reservation_slot.as_time()
            reservation.duration = duration
            reservation.save()

            messages.add_message(
                request, messages.SUCCESS,
                # TODO: Better message
                f'Reservation complete! {reservation}'
            )

    return HttpResponseRedirect(reverse('reservations'))


@login_required
def delete_reservation(request, id):
    """
    The delete_reservation endpoint, which deletes a reservation and redirects
    to the reservations page
    """
    if request.method == "POST":
        reservation = get_object_or_404(Reservation, pk=id)

        if reservation.customer == request.user:
            reservation.delete()
            messages.add_message(
                request, messages.SUCCESS,
                # TODO: Better message
                f'Reservation deleted! {reservation}'
            )

    return HttpResponseRedirect(reverse('reservations'))
