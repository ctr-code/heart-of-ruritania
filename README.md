# The Heart of Ruritania

A warm welcome awaits at The Heart of Ruritania, the UK's first Ruritanian restaurant.

[Learn more and book online at our website](https://ruritania-a4a079b504db.herokuapp.com/).

## Screenshot

![](docs/overview.png)

## Features

For customers the main features are:

* Browse the menu
* Check the opening hours
* Manage reservations
* See contact details

For colleagues the additional features are:

* Add, edit and delete dishes from the menu
* Toggle dishes on and off
* Rearrange the order of dishes on the menu
* Review all the reservations on a given day
* Delete reservations

Using the admin panel the admin can also:

* Manage the restaurant opening hours (both the weekly defaults and exceptions)
* Manage the available tables
* Manage the courses on the menu

## User Roles and Stories

### Roles

* Browser - a casual user browsing the site without logging in
* User - a registered user
* Colleague - a member of the restaurant's staff
* Admin - the restaurant manager

### Completed Stories

* As a browser I can view the menu so that I can plan my meal
* As a browser I can check opening hours so that I know if the restaurant is available
* As a browser I can find contact details so that I can get my questions answered
* As a browser I can create an account so that I can make a reservation
* As a user I can log in so that I can check my reservations
* As a user I can update my account details so that I can be contacted if needed
* As a user I can make a reservation so that I will be sure to get a table
* As a user I can check my reservations so that I don't miss my meal
* As a user I can delete a reservation so that I don't waste the restaurant's time
* As an admin I can set opening hours so that users can automatically book
* As a colleague I can manage reservations so that I can remove griefers
* As a colleague I can view an overview of the day so that I know how busy we'll be
* As a colleague I can edit the menu so that I can keep the site up-to-date without a web developer
* As a colleague I can preview the menu so that I can see what it looks like to a regular user

### Deferred Stories

* As a user I can leave feedback so that the restaurant will improve
* As a user I can make contact through a form so that I'm saved the bother of calling
* As a user I can leave a review so that other people can learn from my experience
* As a colleague I can view an overview calendar so that I know how busy we are for the coming week
* As a colleague I can view a service overview so that I can check reservations as diners arrive
* As an admin I can add stories to a news feed so that customers get a sense of continuous improvement
* As an admin I can set the time zone so that so that the software can be used by businesses outside the UK

## Data Model

### Reservations

``` mermaid
erDiagram
    User ||--o{ Reservation : booked
    User {
        int user_id PK
        string name
        string email
        string first_name
        string last_name
        string phone_number
    }
    Reservation {
        int reservation_id PK
        string svc_date
        string res_date
        string time
        int duration "minutes"
        int guest_count
        int status
        int user_id FK
    }
    Table {
        int table_id PK
        int table_number UK
        int seat_count
    }
    ServiceTime {
        int hours_id PK
        int day_of_week "0-mon to 6-sun"
        string start_time "24-hour clock"
        string end_time "24-hour clock"
    }
    ServiceException {
        int exception_id PK
        string date
        string start_time "24-hour clock"
        string end_time "24-hour clock"
    }
```

If Reservations are proactively mapped to Tables you can arrive in a situation where there is always a table free but never for long enough to accept a booking, so the restaurant capacity is underutilised.

To achieve an optimal mapping reservations need to be mapped to tables every time the reservations change.  Since it needs to be recalculated repeatedly there is little point in keeping the mapping in the database.

### Menu

``` mermaid
erDiagram
    Course ||--o{ Dish : features
    Course {
        int course_id PK
        string name
        int order
    }
    Dish {
        int dish_id PK
        bool active
        int price "pence"
        string name
        string description
        int order
    }
```

The active field on dishes makes it simple to add and remove items from the menu for seasonal availability, say.

## UX Design

### Visual Design

The overall theme is intended to convey tradition and quality.

The textured background is reminiscent of parchment.  Text uses the PT Serif font for a vintage, serious feel.  The whole is suggestive of a menu on quality paper.

The hero image on the home page, in the style of Brueghel, evokes traditional Europe; the cabbages and sausages represent the cuisine while introducing a little whimsy.

The simple palette has colours for parchment and text and highlight colours for the calendar.

![](docs/palette.png)

### Other

The main goal was to make it very easy for the user to manage reservations.

* To make a reservation: click on a date; enter the number of guests; click on a time.  Done.
* To edit a reservation: click on a date; click on a new time.  Done.

This does prevent the creation of multiple reservations on a single day.  However, this is a niche requirement so keeping the interface simple for the typical user was the priority.  A user who really wants multiple reservations can always phone the restaurant.

|Screen|Mobile|Tablet|Desktop|
|-|-|-|-|
|Calendar|![](docs/wire-504/calendar.png)|![](docs/wire-768/calendar.png)|![](docs/wire-992/calendar.png)|
|Time|![](docs/wire-504/reservation-edit.png)|![](docs/wire-768/reservation-edit.png)|![](docs/wire-992/reservation-edit.png)|

The user also needs to be able to check the menu, the opening hours and find contact details.

|Screen|Mobile|Tablet|Desktop|
|-|-|-|-|
|Menu|![](docs/wire-504/menu.png)|![](docs/wire-768/menu.png)|![](docs/wire-992/menu.png)|
|Hours|![](docs/wire-504/hours.png)|![](docs/wire-768/hours.png)|![](docs/wire-992/hours.png)|
|Contact|![](docs/wire-504/contact.png)|![](docs/wire-768/contact.png)|![](docs/wire-992/contact.png)|

An additional goal was to allow the restaurateur to edit the menu for seasonal changes, for example.  Rather than editing the user-visible menu one dish at a time, the manager can create multiple inactive dishes and then enable/disable them all together on the toggle page.

|Screen|Mobile|Tablet|Desktop|
|-|-|-|-|
|Menu admin|![](docs/wire-504/menu-admin.png)|![](docs/wire-768/menu-admin.png)|![](docs/wire-992/menu-admin.png)|
|Add dish|![](docs/wire-504/dish-add.png)|![](docs/wire-768/dish-add.png)|![](docs/wire-992/dish-add.png)|
|Edit dish|![](docs/wire-504/dish-edit.png)|![](docs/wire-768/dish-edit.png)|![](docs/wire-992/dish-edit.png)|
|Toggle dishes|![](docs/wire-504/dishes-arrange.png)|![](docs/wire-768/dishes-arrange.png)|![](docs/wire-992/dishes-arrange.png)
|Arrange dishes|![](docs/wire-504/dishes-arrange.png)|![](docs/wire-768/dishes-arrange.png)|![](docs/wire-992/dishes-arrange.png)

### Security

When the user can naturally navigate to a resource they lack access to (e.g. the reservations page while logged out) the user will be prompted to log in and redirected to their intended destination.

When the server is asked to do an action on a missing resource (e.g. delete a non-existent dish from the menu), the server assumes it must have been deleted and shows a message to this effect.

When the server receives an "impossible" request (such as a GET on a POST-only endpoint) this must have been the result of shenanigans so it is redirected without a message.

## Technology

### Overview

The project is a web application developed using the Django backend web framework.

The Django framework uses the Python lanaguage to dynamically generate HTML pages.
Styling is provided by Bootstrap with some custom CSS.
A little JavaScript provides client-side interactivity.

In addition to the Django core and its dependencies the project uses a number of additional Python libraries:

* [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) and [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5) to automatically format forms with bootstrap
* [dotenv](https://github.com/pedroburon/dotenv) and [python-dotenv](https://pypi.org/project/python-dotenv/) to read environment variables from `.env`
* [dj-database-url](https://jazzband.co/projects/dj-database-url) to parse database URLs
* [django-allauth](https://allauth.org) to authenticate end-users
* [gunicorn](https://gunicorn.org) to serve the content over HTTP
* [psycopg2-binary](https://psycopg.org/) to connect to the PostgreSQL database
* [whitenoise](https://whitenoise.readthedocs.io/en/latest/) to serve static files via WSGI

### Database

The deployed project requires access to a PostgreSQL database instance in the cloud.

For development it is possible to use a local database instance, either PostgreSQL or SQLite, but these instructions assume a cloud instance.

Many companies offer PostgreSQL (or PostgreSQL-compatible) cloud database instances and most require payment.  [Neon](https://neon.com/pricing) has a generous free tier.

To create a cloud database you need to:

1. Choose a cloud PostgreSQL database provider.
2. Create an account.
3. Create a database - you will receive a database URL.
4. Store the URL somewhere safe - it provides complete access to the live database.

The database URL should be something like:

`postgresql://neondb_owner:ngy_rtfGRGRg56g@battery-horse-staple-56dfdf7.c-6.eu-central-1.aws.neon.tech/nuncle_pig_654321`

In the following sections you will copy your database URL into your `.env` file for local development and into your Heroku app config vars for deployment.

### Fork

To develop or deploy this project you first need to fork it on GitHub.

1. Login to your GitHub account.
2. Navigate to [The Heart of Ruritania on GitHub](https://github.com/ctr-code/heart-of-ruritania/).
3. Click on the Fork button (on the right, near the top).
4. The `Create a new fork` page opens.
5. Click on `Create fork`.

### Develop

This section describes how to configure your environment to run the project locally.

The instructions work on Linux, WSL and maybe the VSCode bash prompt, but that's untested.

Having [forked the project](#fork), open a terminal, switch to a suitable parent directory and run this command with your github username:

```bash
git clone https://github.com/<your-github-username>/heart-of-ruritania/
```

Then run:

```bash
cd heart-of-ruritania
python3 -m venv .venv
source .venv/bin/activate
echo "DJANGO_DEBUG = True" > .env
echo "DJANGO_SECRET_KEY = 'somerubbishhere'" >> .env
echo "DJANGO_ALLOWED_HOSTS = '127.0.0.1'" >> .env
echo "DATABASE_URL = 'put_database_url_here'" >> .env
pip install -r requirements.txt
mkdir fixtures
curl -L "https://github.com/validator/validator/releases/download/latest/vnu.jar" > fixtures/vnu.jar
```

Edit the `.env` file to include the [database url created previously](#database).  Install the database schema with:

```bash
./manage.py migrate
```

And start the local webserver with:

```bash
./manage.py runserver
```

### Deploy to Heroku

Having [forked the project](#fork) and [created a database](#database).

1. Create a Heroku account.
2. Login to your account dashboard.
3. Click on `New | Create new app`.
4. Choose and enter a name for the new app.
5. Choose a location (probably Europe).
6. Click on `Create App`.
7. Click on the `Open App` button.
8. Make a note of the host name (something like `blah-1a2b3c4d5e6f.herokuapp.com`).
9. Open the `Settings` tab.
10. Click on `Reveal Config Vars`.
11. Enter the [database url created earlier](#database) as `DATABASE_URL`.
12. Enter the host name from step 8 as `DJANGO_ALLOWED_HOSTS`.
13. Enter some random data as `DJANGO_SECRET_KEY`.
14. Open the `Deploy` tab.
15. Choose `GitHub - Connect to GitHub`.
16. Connect to your GitHub user account and select `heart-of-ruritania`.
17. Click on `Connect`.
18. Click on `Deploy`.
19. Click on `Open App`.
20. Enjoy!

## Copilot AI Assistance

### Misc

Copilot was used to create the hero image and much of the menu.  It was also used to convert the menu from markdown into Django `dumpdata` format to get the menu into the database.

### Coding

Copilot was used for coding in a number of areas.  For example, it converted the entity-relationship diagrams into Django models and it generated much of the code (forms and views) for managing dishes.

### Debugging

When trying to book a table the server threw a 500 error.  Copilot was asked to investigate.  Copilot identified that the problem arose when there was no table available and the code attempted to take the maximum of an empty list.  Copilot fixed the problem.

### Performance and UX

Copilot was asked to suggest UX improvements.  It made a number of solid suggestions such as adding more explanatory text and making telephone numbers clickable, which it was able to implement.  The key suggestion was to make the calendar control more accessible, but this will have to wait for the next sprint.

### Unit Tests

Copilot was used to create a suite of tests for the menu app.  They were fairly comprehensive and mostly sensible but there were some problems.  For example, the toggle dishes test set the items to their original state, so the code could have done nothing and passed.  Neither did it test that items can be disabled.  While generating the tests Copilot noted that there was another potential bug taking the maximum over an empty set, but didn't generate a test for it.  These issues are all fixed now.

### Reflections

I found that Copilot provides very useful reviews.  For example, it reviewed the code comments and I made extensive changes to make them more understandable.  I also had some success asking it to review its own code.

It is very good at producing boilerplate, especially tests, and converting data from one format to another.

Its code is generally verbose and often correct.  When it gets something wrong it is often quicker to fix it yourself than to try to persuade Copilot that there's a problem.

Overall it is a very useful tool that was able to do many of the more tedious tasks.  I particularly appreciated it for the unit testing.

## Testing

Details can be found on the [testing page](TESTING.md).

## Bugs

* django-admin trying to dump data.
* Favicon load failure was on 500 and admin pages.
* Reservations after midnight.
* Menu closer.
* Error if all the tables were used (max over no elements)
* Validation error in signup form needed switch to crispy because of `<ul>` in `<span>`.
* Admin couldn't delete other reservations!

## Credit and Thanks

* [Code Institute](https://codeinstitute.net/) and its tutors for teaching, support and the navbar collapser
* [West Midlands Combined Authority](https://www.wmca.org.uk/) for funding the course
* [Tim Berners-Lee](https://www.w3.org/People/Berners-Lee/) *et al* for the web
* [Brendan Eich](https://en.wikipedia.org/wiki/Brendan_Eich) *et al* for JavaScript
* [Linus Torvalds](https://en.wikipedia.org/wiki/Linus_torvalds) *et al* for Linux
* [Guido van Rossum](https://gvanrossum.github.io/) *et al* for Python
* [The PostgreSQL Authors](https://www.postgresql.org/docs/current/history.html) for the database
* [GitHub](https://github.com/) for hosting the repository and the project plan
* [Heroku](https://www.heroku.com/) for hosting the site
* [Neon](https://neon.com/) for hosting PostgreSQL
* [The Django Authors](https://github.com/django/django/blob/main/AUTHORS) for the web framework
* [Bootstrap](https://getbootstrap.com/) for the CSS framework
* [ParaType](https://www.paratype.com/) for the PT Serif font
* [Font Awesome](https://fontawesome.com/) for icons
* [Fort Awesome](https://github.com/FortAwesome/Font-Awesome/releases) for collating the Font Awesome assets
* [Bunny CDN](https://fonts.bunny.net/) for font hosting
* [Microsoft](https://www.microsoft.com/) for [Visual Studio Code](https://code.visualstudio.com/)
* [Copilot](https://copilot.microsoft.com/) for various tasks as described above
* [W3C](https://www.w3.org/) for the [HTML and CSS validator](https://github.com/validator/validator/)
* [Code Institute](https://pep8ci.herokuapp.com/) again for the Python validator
* [JSHint](https://jshint.com/) for the JavaScript validator
* [WebAIM](https://webaim.org/) for the [WAVE accessibility extension](https://wave.webaim.org/extension/)
* [Inkscape](https://inkscape.org/) for rendering the logo and favicons
* [GIMP](https://www.gimp.org/) for cropping many screenshots
* [Coolors](https://coolors.co/) for the palette generator
* [Fireship](https://fireship.dev/amiresponsive) for the multi-device screenshot
* [MeshSVG.com](https://meshsvg.com/textures/#1.eyJ2IjoxLCJtb2RlIjoidGV4dHVyZSIsInNlZWQiOjEyMzQsInBhbGV0dGUiOlsiIzhiNWNmNiIsIiMyMmQzZWUiXSwicGFyYW1zIjp7InJlY2lwZSI6InBhcGVyIiwidGlsZSI6MjU2LCJpbnRlbnNpdHkiOjAuODYsImNvbG9yMSI6IiNlNWRmODciLCJjb2xvcjIiOm51bGwsInRleHR1cmVTZWVkIjoxMjM0fX0) for the background texture
* [Raymond1922A](https://commons.wikimedia.org/wiki/File:Flag_of_Prussia_without_regalia.svg) for the Prussian eagle
