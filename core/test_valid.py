from django.urls import reverse
from django.conf import settings
from core.common_test import TestValidHtml


class TestValidPages(TestValidHtml):
    """
    Check that all the core pages have valid HTML and check style.css
    """

    def test_validate_css(self):
        self.assertValidCSS(settings.BASE_DIR / 'static/css/style.css')

    def test_validate_page_home(self):
        self.assertValid(reverse('index'))

    def test_validate_page_contact(self):
        self.assertValid(reverse('contact'))
