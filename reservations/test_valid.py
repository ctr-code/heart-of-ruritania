from datetime import date, time, timedelta
from core.common_test import TestValidHtml
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ServiceTime, ServiceException, Table


class TestValidPages(TestValidHtml):
    """
    Check that all the menu pages have valid HTML
    """

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        User.objects.create_user(
            username="regularJoe",
            password="myPassword",
            email="test@test.com"
        )
        Table.objects.create(
            table_number=1,
            cover_count=4
        )
        for dow in range(0, 7):
            ServiceTime.objects.create(
                weekday=dow,
                start_time=time(11, 30),
                end_time=time(15, 30)

            ).save()
            ServiceTime.objects.create(
                weekday=dow,
                start_time=time(17, 30),
                end_time=time(21, 30)
            ).save()
        self.today = date.today()
        ServiceException.objects.create(
            date=self.today + timedelta(days=2),
            open=False
        ).save()
        ServiceException.objects.create(
            date=self.today + timedelta(days=3),
            open=True,
            start_time=time(15, 00),
            end_time=time(19, 45)
        ).save()

    def test_validate_page_hours(self):
        self.assertValid(reverse('hours'))

    def test_validate_page_reservations(self):
        self.client.login(
            username="regularJoe", password="myPassword")
        self.assertValid(reverse('reservations'))

    def test_validate_page_reservation_times(self):
        self.client.login(
            username="regularJoe", password="myPassword")
        day = self.today + timedelta(days=1)
        self.assertValid(reverse(
            'reservation_times',
            args=[day.year, day.month, day.day]
        ))

    def test_validate_page_reservations_admin(self):
        self.client.login(
            username="myUsername", password="myPassword")
        self.assertValid(reverse('admin_calendar'))

    def test_validate_page_admin_day(self):
        self.client.login(
            username="myUsername", password="myPassword")
        day = self.today
        self.assertValid(reverse(
            'admin_day',
            args=[day.year, day.month, day.day]
        ))
