from django.contrib.auth.models import User
from django.urls import reverse
from core.common_test import TestValidHtml
from .models import Course, Dish


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
        self.mains = Course.objects.create(name="Mains", order=2)
        self.mains.save()
        self.sausages = Dish.objects.create(
            course=self.mains,
            active=True,
            price=2350,
            name="Sausages",
            description="Tasty.",
            order=1
        )
        self.sausages.save()
        self.carrots = Dish.objects.create(
            course=self.mains,
            active=True,
            price=2350,
            name="Carrots",
            description="Tasty.",
            order=2
        )
        self.carrots.save()
        self.peas = Dish.objects.create(
            course=self.mains,
            active=True,
            price=2350,
            name="Peas",
            description="Tasty.",
            order=3
        )
        self.peas.save()

    def test_validate_page_menu(self):
        self.assertValid(reverse('menu'))

    def test_validate_page_menu_admin(self):
        self.client.login(
            username="myUsername", password="myPassword")
        self.assertValid(reverse('menu_admin'))

    def test_validate_page_add_dish(self):
        self.client.login(
            username="myUsername", password="myPassword")
        self.assertValid(reverse('add_dish', args=[self.mains.id]))

    def test_validate_page_edit_dish(self):
        self.client.login(
            username="myUsername", password="myPassword")
        self.assertValid(reverse('edit_dish', args=[self.sausages.id]))

    def test_validate_page_arrange_dishes(self):
        self.client.login(
            username="myUsername", password="myPassword")
        self.assertValid(reverse('arrange_dishes', args=[self.mains.id]))

    def test_validate_page_toggle_dishes(self):
        self.client.login(
            username="myUsername", password="myPassword")
        self.assertValid(reverse('toggle_dishes', args=[self.mains.id]))
