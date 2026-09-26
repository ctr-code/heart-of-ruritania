# The Heart of Ruritania - Testing

Validation of HTML, CSS, JS, Python

Lighthouse

## User Stories

* As a browser I can view the menu so that I can plan my meal
* As a browser I can check opening hours so that I know if the restaurant is available
* As a browser I can find contact details so that I can get my questions answered
* As a browser I can create an account so that I can make a reservation
* As a user I can log in so that I can check my reservations
* As a user I can update my account details so that I can be contacted if needed
* As a user I can make a reservation so that I will be sure to get a table
* As a user I can check my reservations so that to remind myself
* As a user I can delete a reservation so that I don't waste the restaurant's time
* As an admin I can set opening hours so that users can automatically book
* As an admin I can manage reservations so that I can remove griefers
* As a colleague I can view an overview of the day so that I know how busy we'll be
* As an admin I can edit the menu so that I can keep the site up-to-date without a web developer
* As an admin I can preview the menu so that I can see what it looks like to a regular user

### Google Lighthouse Performance

Desktop | Mobile
-- | --
![Lighthouse for desktop](docs/lighthouse-desktop.png) | ![Lighthouse for mobile](docs/lighthouse-mobile.png)

## Automated Testing

Run `python3 manage.py test`.  At the moment this only does the W3C validation.  Screenshot:

![](docs/python-tests.png)|

## HTML and CSS validation

This is handled automatically as part of the Python testing.

To demonstrate that it does something, this is the output of a previously failing test.  The problematic URL and the validation errors appear at the end:

```
FAIL: test_validate_page_edit_dish (menu.test_valid.TestValidPages.test_validate_page_edit_dish)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ci/progs/ruritania/menu/test_valid.py", line 64, in test_validate_page_edit_dish
    self.assertValid(reverse('edit_dish', args=[self.sausages.id]))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ci/progs/ruritania/core/common_test.py", line 31, in assertValid
    self.assertTrue(
    ~~~~~~~~~~~~~~~^
        result.returncode == 0,
        ^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
        )
        ^
    )
    ^
AssertionError: False is not true : The HTML is not valid
/menu/dish/1/edit
:127.1-127.109: error: The “aria-labelledby” attribute must not be specified on any “div” element unless the element has a “role” value other than “caption”, “code”, “deletion”, “emphasis”, “generic”, “insertion”, “paragraph”, “presentation”, “strong”, “subscript”, or “superscript”.
:142.21-142.79: error: Attribute “href” not allowed on element “button” at this point.
:131.17-131.62: error: The heading “h3” (with computed level 3) follows the heading “h1” (with computed level 1), skipping 1 heading level.
```

## JavaScript Validation

JavaScript was validated using [JSHint](https://jshint.com/).

|JavaScript File|Validation Results|
|-|-|
|[core/static/js/profile.js](core/static/js/profile.js)|![](docs/js-valid/profile.png)|
|[menu/static/js/arrange_dishes.js](menu/static/js/arrange_dishes.js)|![](docs/js-valid/arrange_dishes.png)|
|[menu/static/js/edit_dish.js](menu/static/js/edit_dish.js)|![](docs/js-valid/edit_dish.png)|
|[reservations/static/js/admin_day.js](reservations/static/js/admin_day.js)|![](docs/js-valid/admin_day.png)|
|[reservations/static/js/reservation_times.js](reservations/static/js/reservation_times.js)|![](docs/js-valid/reservation_times.png)|
|[templates/base.html](templates/base.html)|![](docs/js-valid/hamburger.png)|

## Python Validation

Python was validated using [testshot](https://github.com/ctr-code/testshot).

|Python File|Validation Results|
|-|-|
|[core/common_test.py](core/common_test.py)|![](docs/py-valid/core-common_test.png)|
|[core/forms.py](core/forms.py)|![](docs/py-valid/core-forms.png)|
|[core/test_valid.py](core/test_valid.py)|![](docs/py-valid/core-test_valid.png)|
|[core/views.py](core/views.py)|![](docs/py-valid/core-views.png)|
|[menu/admin.py](menu/admin.py)|![](docs/py-valid/menu-admin.png)|
|[menu/forms.py](menu/forms.py)|![](docs/py-valid/menu-forms.png)|
|[menu/models.py](menu/models.py)|![](docs/py-valid/menu-models.png)|
|[menu/templatetags/menu.py](menu/templatetags/menu.py)|![](docs/py-valid/menu-templatetags-menu.png)|
|[menu/test_valid.py](menu/test_valid.py)|![](docs/py-valid/menu-test_valid.png)|
|[menu/urls.py](menu/urls.py)|![](docs/py-valid/menu-urls.png)|
|[menu/views.py](menu/views.py)|![](docs/py-valid/menu-views.png)|
|[reservations/admin.py](reservations/admin.py)|![](docs/py-valid/reservations-admin.png)|
|[reservations/forms.py](reservations/forms.py)|![](docs/py-valid/reservations-forms.png)|
|[reservations/models.py](reservations/models.py)|![](docs/py-valid/reservations-models.png)|
|[reservations/test_valid.py](reservations/test_valid.py)|![](docs/py-valid/reservations-test_valid.png)|
|[reservations/timerange.py](reservations/timerange.py)|![](docs/py-valid/reservations-timerange.png)|
|[reservations/urls.py](reservations/urls.py)|![](docs/py-valid/reservations-urls.png)|
|[reservations/views.py](reservations/views.py)|![](docs/py-valid/reservations-views.png)|
|[ruritania/settings.py](ruritania/settings.py)|![](docs/py-valid/ruritania-settings.png)|
|[ruritania/urls.py](ruritania/urls.py)|![](docs/py-valid/ruritania-urls.png)|
