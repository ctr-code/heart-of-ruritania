# The Heart of Ruritania - Testing

## User Stories and Acceptance Critera

The project's key functionality was tested by working through the user stories and ensuring that each one worked.  One or more screenshots illustrate the feature and confirmation messages.

|User Story and Acceptance Criteria|Screenshot|
|-|-|
|As **a browser** I can **view the menu** so that **I can plan my meal**.<br><br>• The website contains the restaurant menu<br>• Every page has a clear link to the menu|![](docs/user-story/1-menu.png)|
|As **a browser** I can **check opening hours** so that **I know if the restaurant is available**.<br><br>• The website displays opening hours<br>• Every page has a clear link to the opening hours|![](docs/user-story/2-hours.png)|
|As **a browser** I can **find contact details** so that **I can get my questions answered**.<br><br>• The website has a page of contact information<br>• Every page has a clear link to the contact page|![](docs/user-story/3-contact.png)|
|As **a browser** I can **create an account** so that **I can make a reservation**.<br><br>• When nobody is logged-in every page has a clear link to the Register page<br>• The Register page asks for details and creates an account|![](docs/user-story/4-register.png)|
||![](docs/user-story/4-register-confirm.png)|
|As **a user** I can **log in** so that **I can check my reservations**.<br><br>• When nobody is logged-in every page has a clear link to the Login page<br>• The Login page asks for details, verifies them and logs the user in|![](docs/user-story/5-login.png)|
||![](docs/user-story/5-login-confirm.png)|
|As **a user** I can **update my account details** so that **I can be contacted if needed**.<br><br>• When a user is logged-in every page has a clear link to the Profile page<br>• The Profile page lets the user edit their details|![](docs/user-story/6-profile.png)|
||![](docs/user-story/6-profile-confirm.png)|
|As **a user** I can **make a reservation** so that **I will be sure to get a table**.<br><br>• Every page has a clear link to the reservation page<br>• Browsers are prompted to login<br>• Users are presented with a calendar so they can pick a date<br>• They are then prompted with a grid of available times to select one|![](docs/user-story/7-reservations.png)|
||![](docs/user-story/7-reservations-time.png)|
||![](docs/user-story/7-reservations-confirm.png)|
|As **a user** I can **check my reservations** so that **I don't miss my meal**.<br><br>• The reservations calendar highlights dates with reservations<br>• The edit reservation page highlights the reserved time slot|![](docs/user-story/8-check-reservation.png)|
||![](docs/user-story/8-check-reservation-time.png)|
|As **a user** I can **delete a reservation** so that **I don't waste the restaurant's time**.<br><br>• The edit reservation page has a delete button<br>• The user is prompted for confirmation before deleting the reservation|![](docs/user-story/9-delete-reservation.png)|
||![](docs/user-story/9-delete-reservation-confirm.png)|
|As **an admin** I can **set opening hours** so that **users can automatically book**.<br><br>• Opening hours can be edited in the Admin panel|![](docs/user-story/10-admin-times.png)|
|As **a colleague** I can **view an overview of the day** so that **I know how busy we'll be**.<br><br>• The day overview shows all the reservations.|![](docs/user-story/11-day-overview.png)|
|As **a colleague** I can **manage reservations** so that **I can remove griefers**.<br><br>• Reservations can be deleted in the admin day overview.|![](docs/user-story/12-admin-day-delete.png)|
||![](docs/user-story/12-admin-day-delete-confirm.png)|
|As **a colleague** I can **edit the menu** so that **I can keep the site up-to-date without a web developer**.<br><br>• Each menu section has a button to create a new dish in that section<br>• Each dish has buttons to edit, delete and toggle (enable/disable) it|![](docs/user-story/13-menu-admin.png)|
||![](docs/user-story/13-menu-add.png)|
||![](docs/user-story/13-menu-add-confirm.png)|
||![](docs/user-story/13-menu-toggle.png)|
||![](docs/user-story/13-menu-toggle-confirm.png)|
||![](docs/user-story/13-menu-arrange.png)|
||![](docs/user-story/13-menu-arrange-confirm.png)|
|As **a colleague** I can **preview the menu** so that **I can see what it looks like to a regular user**.<br><br>• The menu link in the navbar leads to the menu admin page<br>• The menu admin page has a link to the regular menu page|![](docs/user-story/14-menu-preview.png)|

## Unit Tests

The tests cover two areas:

* The menu application: viewing, adding, editing, toggling, arranging and deleting dishes.
* Validation of the HTML and CSS using the offline W3C validator.

Execute `python3 manage.py test` to run the tests:

![](docs/python-tests.png)

## Defence

All of the views were identified along with their inputs, and each one was exercised with missing or invalid data.  Screenshots illustrate the results.

Much of the server-side validation will not be seen ordinarily but it may be required if the user has an old browser.

A chunk of this is covered by the unit tests, which were added belatedly.

### Signup

[https://ruritania-a4a079b504db.herokuapp.com/accounts/signup/](https://ruritania-a4a079b504db.herokuapp.com/accounts/signup/)

|Description|Screenshot|
|-|-|
|Missing user|![](docs/defence/1-register-user.png)|
|Missing password|![](docs/defence/1-register-password.png)|
|Missing second password field|![](docs/defence/1-register-password2.png)|
|The passwords don't match|![](docs/defence/1-register-mismatch.png)|
|Bad password|![](docs/defence/1-register-bad.png)|
|Server-side validation|![](docs/defence/1-register-server.png)|

### Login

[https://ruritania-a4a079b504db.herokuapp.com/accounts/login/](https://ruritania-a4a079b504db.herokuapp.com/accounts/login/)

|Description|Screenshot|
|-|-|
|Missing user|![](docs/defence/2-login-user.png)|
|Missing password|![](docs/defence/2-login-password.png)|
|Wrong password|![](docs/defence/2-login-wrong.png)|
|Server-side validation|![](docs/defence/2-login-server.png)|

### Profile

[https://ruritania-a4a079b504db.herokuapp.com/profile](https://ruritania-a4a079b504db.herokuapp.com/profile)

|Description|Screenshot|
|-|-|
|Missing email|![](docs/defence/3-profile-email.png)|
|Invalid email address|![](docs/defence/3-profile-email-valid.png)|
|Server-side validation|![](docs/defence/3-profile-server.png)|
|Server-side validation|![](docs/defence/3-profile-server-email.png)|

### Menu Admin

[https://ruritania-a4a079b504db.herokuapp.com/menu/admin](https://ruritania-a4a079b504db.herokuapp.com/menu/admin)

|Description|Screenshot|
|-|-|
|Not logged in|![](docs/defence/6-menu-admin-out.png)|
|Logged in as a customer|![](docs/defence/6-menu-admin-cust.png)|

### Add Dish

[https://ruritania-a4a079b504db.herokuapp.com/menu/course/1/add](https://ruritania-a4a079b504db.herokuapp.com/menu/course/1/add)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/4-dish-add-out.png)|
|Logged in as a customer|![](docs/defence/4-dish-add-cust.png)|
|[Add dish with invalid course id](https://ruritania-a4a079b504db.herokuapp.com/menu/course/994/add)|![](docs/defence/bad-course-id.png)|
|Missing name|![](docs/defence/4-dish-add-name.png)|
|Missing description|![](docs/defence/4-dish-add-desc.png)|
|Missing price|![](docs/defence/4-dish-add-price.png)|
|Server-side validation|![](docs/defence/4-dish-add-server.png)|
|Server-side validation|![](docs/defence/4-dish-add-server-price.png)|

### Edit Dish

[https://ruritania-a4a079b504db.herokuapp.com/menu/dish/54/edit](https://ruritania-a4a079b504db.herokuapp.com/menu/dish/54/edit)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/5-dish-edit-out.png)|
|Logged in as a customer|![](docs/defence/5-dish-edit-cust.png)|
|[Edit dish with invalid id](https://ruritania-a4a079b504db.herokuapp.com/menu/dish/995/edit)|![](docs/defence/bad-dish-id.png)|
|Missing name|![](docs/defence/5-dish-edit-name.png)|
|Missing description|![](docs/defence/5-dish-edit-desc.png)|
|Missing price|![](docs/defence/5-dish-edit-price.png)|
|Non-numeric price|![](docs/defence/5-dish-edit-price2.png)|
|Server-side validation|![](docs/defence/5-dish-edit-server.png)|
|Server-side validation|![](docs/defence/5-dish-edit-server-price.png)|
|Attempt to delete a dish that another user just deleted|![](docs/defence/5-dish-edit-deleted.png)|

### Toggle Dishes

[https://ruritania-a4a079b504db.herokuapp.com/menu/course/1/toggle](https://ruritania-a4a079b504db.herokuapp.com/menu/course/1/toggle)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/7-course-toggle-out.png)|
|Logged in as a customer|![](docs/defence/7-course-toggle-cust.png)|
|[Edit course with invalid course id](https://ruritania-a4a079b504db.herokuapp.com/menu/course/837/toggle)|![](docs/defence/bad-course-id.png)|

### Arrange Dishes

[https://ruritania-a4a079b504db.herokuapp.com/menu/course/1/arrange](https://ruritania-a4a079b504db.herokuapp.com/menu/course/1/arrange)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/7-course-arrange-out.png)|
|Logged in as a customer|![](docs/defence/7-course-arrange-cust.png)|
|[Arrange course with invalid course id](https://ruritania-a4a079b504db.herokuapp.com/menu/course/996/arrange)|![](docs/defence/bad-course-id.png)|

### Reservations

[https://ruritania-a4a079b504db.herokuapp.com/reservations](https://ruritania-a4a079b504db.herokuapp.com/reservations)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/8-res-out.png)|

### Reservation Times

In these two cases the server simply redirects to the reservations page so there is nothing to show:

* [A day when the restaurant is closed](https://ruritania-a4a079b504db.herokuapp.com/reservations/2026-11-25)
* [A day outside the booking period](https://ruritania-a4a079b504db.herokuapp.com/reservations/2027-9-25)

An attempt to delete another user's reservation is handled similarly.

[https://ruritania-a4a079b504db.herokuapp.com/reservations/2026-11-26](https://ruritania-a4a079b504db.herokuapp.com/reservations/2026-11-26)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/8-res-time-out.png)|
|The reservation failed.  This happens if the last table has just been taken by another user, or if the user created a bogus request using the browser dev tools, say.|![](docs/defence/8-res-stolen.png)|
|The reservation had already been deleted, perhaps by an admin.  The same endpoint is used for both users and admins so this check also works for admin deletions.|![](docs/defence/8-res-deleted.png)|

### Reservations Admin

[https://ruritania-a4a079b504db.herokuapp.com/reservations/admin](https://ruritania-a4a079b504db.herokuapp.com/reservations/admin)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/9-res-admin-out.png)|
|Logged in as a customer|![](docs/defence/9-res-admin-cust.png)|

### Reservations Admin Day View

[https://ruritania-a4a079b504db.herokuapp.com/reservations/2026-11-26/admin](https://ruritania-a4a079b504db.herokuapp.com/reservations/2026-11-26/admin)

|Description|Screenshot|
|-|-|
|Logged out|![](docs/defence/9-res-time-admin-out.png)|
|Logged in as a customer|![](docs/defence/9-res-time-admin-cust.png)|

The only interactivity here is the Delete button, which, as noted in the previous section, uses the same endpoint as non-admin users so it has been tested.

## Google Lighthouse Performance

Desktop | Mobile
-- | --
![Lighthouse for desktop](docs/lighthouse-desktop.png) | ![Lighthouse for mobile](docs/lighthouse-mobile.png)

## Responsivity

This section demonstrates the responsivity of the site with screenshots for mobile, tablet and desktop views.

|Page|Mobile|Tablet|Desktop|
|-|-|-|-|
||![](docs/resp/mobile/index.png)|![](docs/resp/tablet/index.png)|![](docs/resp/desktop/index.png)|
|menu/|![](docs/resp/mobile/menu.png)|![](docs/resp/tablet/menu.png)|![](docs/resp/desktop/menu.png)|
|hours|![](docs/resp/mobile/hours.png)|![](docs/resp/tablet/hours.png)|![](docs/resp/desktop/hours.png)|
|contact|![](docs/resp/mobile/contact.png)|![](docs/resp/tablet/contact.png)|![](docs/resp/desktop/contact.png)|
|reservations|![](docs/resp/mobile/reservations.png)|![](docs/resp/tablet/reservations.png)|![](docs/resp/desktop/reservations.png)|
|reservations/2026-10-30|![](docs/resp/mobile/reservations-2026-10-30.png)|![](docs/resp/tablet/reservations-2026-10-30.png)|![](docs/resp/desktop/reservations-2026-10-30.png)|
|profile|![](docs/resp/mobile/profile.png)|![](docs/resp/tablet/profile.png)|![](docs/resp/desktop/profile.png)|
|reservations/admin|![](docs/resp/mobile/reservations-admin.png)|![](docs/resp/tablet/reservations-admin.png)|![](docs/resp/desktop/reservations-admin.png)|
|reservations/2026-10-1/admin|![](docs/resp/mobile/reservations-2026-10-1-admin.png)|![](docs/resp/tablet/reservations-2026-10-1-admin.png)|![](docs/resp/desktop/reservations-2026-10-1-admin.png)|
|menu/admin|![](docs/resp/mobile/menu-admin.png)|![](docs/resp/tablet/menu-admin.png)|![](docs/resp/desktop/menu-admin.png)|
|menu/course/1/add|![](docs/resp/mobile/menu-course-1-add.png)|![](docs/resp/tablet/menu-course-1-add.png)|![](docs/resp/desktop/menu-course-1-add.png)|
|menu/dish/54/edit|![](docs/resp/mobile/menu-dish-54-edit.png)|![](docs/resp/tablet/menu-dish-54-edit.png)|![](docs/resp/desktop/menu-dish-54-edit.png)|
|menu/course/1/toggle|![](docs/resp/mobile/menu-course-1-toggle.png)|![](docs/resp/tablet/menu-course-1-toggle.png)|![](docs/resp/desktop/menu-course-1-toggle.png)|
|menu/course/1/arrange|![](docs/resp/mobile/menu-course-1-arrange.png)|![](docs/resp/tablet/menu-course-1-arrange.png)|![](docs/resp/desktop/menu-course-1-arrange.png)|
|accounts/login/|![](docs/resp/mobile/accounts-login.png)|![](docs/resp/tablet/accounts-login.png)|![](docs/resp/desktop/accounts-login.png)|

## HTML and CSS validation

As noted previously, the project uses unit tests to generate pages and run them through a local copy of the validator.

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

A page from the live site validated using the W3C online service, to illustrate that it works:

![](docs/valid-menu.png)

## Accessibility

Accessibility was tested using Lighthouse and the [WAVE accessibility extension](https://wave.webaim.org/extension/).

I tested all the pages and I explain the errors and warnings below:

|Gloss|WAVE results|
|-|-|
|All pages have a warning about redundant links because the logo, restaurant name, and Home navbar link all link to the home page.  Many users expect the logo and title to link to the home page; other users will be confused if there is not an explicit Home link.|![](docs/wave/menu-admin.png)|
|Days when the restaurant is closed appear on the calendar with low contrast.  This is by design.<br>WAVE complains of a table used for layout; this should be fixed in the next version.|![](docs/wave/reservations-admin.png)|
|The form contains a hidden button to prevent the form auto-submitting when enter is pressed or when Go is tapped on mobile.  WAVE complains that it has no value text but it is hidden and has the aria-hidden="true" attribute (as WAVE also notes) so the hidden button won't affect screen reader users.<br>The page also uses a table for layout; this should be fixed in the next version.|![](docs/wave/reservation-edit.png)|
|WAVE complains of a table used for layout.  This actually is a table of opening hours so it is fine.|![](docs/wave/hours.png)|

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

Python was validated using the [Code Institute Python validator](https://pep8ci.herokuapp.com/).

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
