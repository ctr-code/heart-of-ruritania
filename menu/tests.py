from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import DishForm
from .models import Course, Dish


class MenuTestDataMixin:
    def create_menu(self):
        self.mains = Course.objects.create(name="Mains", order=2)
        self.desserts = Course.objects.create(name="Desserts", order=1)
        self.sausages = Dish.objects.create(
            course=self.mains,
            active=True,
            price=2350,
            name="Sausages",
            description="Tasty.",
            order=1,
        )
        self.carrots = Dish.objects.create(
            course=self.mains,
            active=False,
            price=1200,
            name="Carrots",
            description="Fresh.",
            order=2,
        )


class MenuModelTests(MenuTestDataMixin, TestCase):
    def setUp(self):
        self.create_menu()

    def test_courses_and_dishes_are_ordered_by_order(self):
        self.assertEqual(
            list(Course.objects.all()), [self.desserts, self.mains]
        )
        self.assertEqual(
            list(self.mains.dishes.all()), [self.sausages, self.carrots]
        )

    def test_string_representations_include_relevant_state(self):
        self.assertEqual(str(self.mains), "Mains")
        self.assertEqual(str(self.sausages), "Sausages (Active)")
        self.assertEqual(str(self.carrots), "Carrots (Inactive)")


class DishFormTests(MenuTestDataMixin, TestCase):
    def setUp(self):
        self.create_menu()

    def test_course_and_order_are_not_editable_form_fields(self):
        form = DishForm(instance=self.sausages)

        self.assertEqual(
            list(form.fields), ["name", "description", "price", "active"]
        )

    def test_price_must_be_a_non_negative_integer(self):
        form = DishForm(
            data={
                "name": "Soup",
                "description": "Hot.",
                "price": "-1",
                "active": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)


class MenuViewTests(MenuTestDataMixin, TestCase):
    def setUp(self):
        self.create_menu()
        self.staff = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.customer = User.objects.create_user(
            username="customer", password="password"
        )

    def test_public_menu_shows_only_active_dishes(self):
        response = self.client.get(reverse("menu"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sausages")
        self.assertNotContains(response, "Carrots")

    def test_staff_views_require_staff_membership(self):
        protected_urls = [
            reverse("menu_admin"),
            reverse("add_dish", args=[self.mains.id]),
            reverse("edit_dish", args=[self.sausages.id]),
            reverse("delete_dish", args=[self.sausages.id]),
            reverse("toggle_dishes", args=[self.mains.id]),
            reverse("arrange_dishes", args=[self.mains.id]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"/admin/login/?next={url}",
                    fetch_redirect_response=False,
                )

    def test_customer_cannot_access_staff_views(self):
        self.client.login(username="customer", password="password")

        response = self.client.get(reverse("menu_admin"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_staff_can_add_dish_and_assign_next_order(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("add_dish", args=[self.mains.id]),
            {
                "name": "Peas",
                "description": "Green.",
                "price": 900,
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("menu_admin"))
        peas = Dish.objects.get(name="Peas")
        self.assertEqual(peas.course, self.mains)
        self.assertEqual(peas.order, 3)
        self.assertTrue(peas.active)

    def test_staff_can_add_dish_to_empty_course(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("add_dish", args=[self.desserts.id]),
            {
                "name": "Raspberries",
                "description": "Tangy.",
                "price": 900,
            },
        )

        self.assertRedirects(response, reverse("menu_admin"))
        raspberries = Dish.objects.get(name="Raspberries")
        self.assertEqual(raspberries.course, self.desserts)
        self.assertEqual(raspberries.order, 1)
        self.assertFalse(raspberries.active)

    def test_staff_can_edit_dish_without_changing_course_or_order(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("edit_dish", args=[self.sausages.id]),
            {
                "name": "Grilled sausages",
                "description": "Extra tasty.",
                "price": 2500,
                "active": "",
            },
        )

        self.assertRedirects(response, reverse("menu_admin"))
        self.sausages.refresh_from_db()
        self.assertEqual(self.sausages.name, "Grilled sausages")
        self.assertEqual(self.sausages.description, "Extra tasty.")
        self.assertEqual(self.sausages.price, 2500)
        self.assertFalse(self.sausages.active)
        self.assertEqual(self.sausages.course, self.mains)
        self.assertEqual(self.sausages.order, 1)

    def test_staff_can_delete_dish(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("delete_dish", args=[self.sausages.id])
        )

        self.assertRedirects(response, reverse("menu_admin"))
        self.assertFalse(Dish.objects.filter(pk=self.sausages.id).exists())

    def test_toggle_updates_only_dishes_present_in_form(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("toggle_dishes", args=[self.mains.id]),
            {
                f"dish_{self.carrots.id}": "",
                f"active_{self.carrots.id}": "on",
            },
        )

        self.assertRedirects(response, reverse("menu_admin"))
        self.sausages.refresh_from_db()
        self.carrots.refresh_from_db()
        self.assertTrue(self.sausages.active)
        self.assertTrue(self.carrots.active)

    def test_toggle_can_disable(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("toggle_dishes", args=[self.mains.id]),
            {
                f"dish_{self.sausages.id}": "",
            },
        )

        self.assertRedirects(response, reverse("menu_admin"))
        self.sausages.refresh_from_db()
        self.carrots.refresh_from_db()
        self.assertFalse(self.sausages.active)
        self.assertFalse(self.carrots.active)

    def test_arrange_updates_orders_for_submitted_dishes(self):
        self.client.login(username="staff", password="password")

        response = self.client.post(
            reverse("arrange_dishes", args=[self.mains.id]),
            {
                f"dish_{self.sausages.id}": 2,
                f"dish_{self.carrots.id}": 1,
            },
        )

        self.assertRedirects(response, reverse("menu_admin"))
        self.sausages.refresh_from_db()
        self.carrots.refresh_from_db()
        self.assertEqual(self.sausages.order, 2)
        self.assertEqual(self.carrots.order, 1)

    def test_missing_course_redirects_from_add_view(self):
        self.client.login(username="staff", password="password")

        response = self.client.get(reverse("add_dish", args=[9999]))

        self.assertRedirects(response, reverse("menu_admin"))

    def test_missing_dish_redirects_from_edit_view(self):
        self.client.login(username="staff", password="password")

        response = self.client.get(reverse("edit_dish", args=[9999]))

        self.assertRedirects(response, reverse("menu_admin"))
