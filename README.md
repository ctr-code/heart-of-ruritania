# The Heart of Ruritania

A warm welcome awaits at The Heart of Ruritania, the UK's first Ruritanian restaurant.

[Learn more and book online at our website](https://ruritania-a4a079b504db.herokuapp.com/).

## Screenshot

## Features

Brief description of website features.

## User Roles and Stories

### Roles

* Browser - a casual user browsing the site without logging in
* User - a registered user
* Colleague - a member of the restaurant's staff
* Admin - the restaurant manager

### Stories

* As a browser I can view the menu so that I can plan my meal
* As a browser I can check opening hours so that I know if the restaurant is available
* As a browser I can find contact details so that I can get my questions answered
* As a browser I can create an account so that I can make a reservation
* As a user I can log in so that I can check my reservations
* As a user I can update my account details so that I can be contacted if needed
* As a user I can make a reservation so that I will be sure to get a table
* As a user I can check my reservations so that to remind myself
* As a user I can delete a reservation so that I don't waste the restaurant's time
* As a user I can leave feedback so that the restaurant will improve
* As a user I can make contact through a form so that I'm saved the bother of calling
* As a user I can leave a review so that other people can learn from my experience
* As an admin I can set opening hours so that users can automatically book
* As an admin I can manage reservations so that I can remove griefers
* As a colleague I can view an overview calendar so that I know how busy we are for the coming week
* As a colleague I can view an overview of the day so that I know how busy we'll be
* As a colleague I can view a service overview so that I can check reservations as diners arrive
* As an admin I can add stories to a news feed so that customers get a sense of continuous improvement
* As an admin I can set the time zone so that so that time-based editing restrictions work correctly

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

### Security

When the user can naturally navigate to a resource they lack access to (e.g. the reservations page while logged out) the user will be prompted to log in and redirected to their intended destination.

When the server receives an "impossible" request (such as one user trying to delete another user's reservation) this must have been the result of shenanigans so it will be quietly ignored.

### Other

Discussion of design choices.  Wireframes.

Only one reservation per day.

Purpose of toggling.

## UI Design

Colours, fonts, images.

## Technologies

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

### Development

This section describes how to configure your environment to work on the project.

The instructions work on Linux, WSL and maybe the VSCode bash prompt, but that's untested.

First of all fork this GitHub repo.  Then open a terminal, switch to a suitable parent directory and run this command with your github username:

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
echo "DATABASE_URL = '<fillmein>'" >> .env
pip install -r requirements.txt
mkdir fixtures
curl -L "https://github.com/validator/validator/releases/download/latest/vnu.jar" > fixtures/vnu.jar
```

Edit the `.env` file to include your actual database url.  Install the database with:

```bash
./manage.py migrate
```

And start the local webserver with:

```bash
./manage.py runserver
```

### Deployment on Heroku

## AI

* Menu suggestions.
* Created Django models from entity-relationship diagrams.
* Converted menu contents from markdown to Django `dumpdata` format to get it into the database.
* Identify code in need of comments.
* Hero image.

## Testing

Details can be found on the [testing page](TESTING.md).

## Bugs

* Favicon load failure
* Reservations after midnight.
* Menu closer.

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
* [Font Awesome](https://fontawesome.com/) for icons
* [Fort Awesome](https://github.com/FortAwesome/Font-Awesome/releases) for collating the Font Awesome assets
* [Bunny CDN](https://fonts.bunny.net/) for font hosting
* [Microsoft](https://www.microsoft.com/) for [Visual Studio Code](https://code.visualstudio.com/)
* [Copilot](https://copilot.microsoft.com/) for various tasks as described above
* [W3C](https://www.w3.org/) for the [HTML and CSS validator](https://github.com/validator/validator/)
* [Inkscape](https://inkscape.org/) for rendering the logo and favicons
* [GIMP](https://www.gimp.org/) for cropping many screenshots
* [Coolors](https://coolors.co/) for the palette generator
* [Fireship](https://fireship.dev/amiresponsive) for the multi-device screenshot
* [Multi Device Mockup Generator](https://techsini.com/multi-mockup/) for the multi-device screenshot
* [MeshSVG.com](https://meshsvg.com/textures/#1.eyJ2IjoxLCJtb2RlIjoidGV4dHVyZSIsInNlZWQiOjEyMzQsInBhbGV0dGUiOlsiIzhiNWNmNiIsIiMyMmQzZWUiXSwicGFyYW1zIjp7InJlY2lwZSI6InBhcGVyIiwidGlsZSI6MjU2LCJpbnRlbnNpdHkiOjAuODYsImNvbG9yMSI6IiNlNWRmODciLCJjb2xvcjIiOm51bGwsInRleHR1cmVTZWVkIjoxMjM0fX0) for the background texture
* [Raymond1922A](https://commons.wikimedia.org/wiki/File:Flag_of_Prussia_without_regalia.svg) for the Prussian eagle
