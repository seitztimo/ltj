[![Build status](https://travis-ci.org/City-of-Helsinki/ltj.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/ltj)
[![codecov](https://codecov.io/gh/City-of-Helsinki/ltj/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/ltj)
[![Requirements](https://requires.io/github/City-of-Helsinki/ltj/requirements.svg?branch=master)](https://requires.io/github/City-of-Helsinki/ltj/requirements/?branch=master)

# City of Helsinki nature database and API (LTJ)

LTJ is a backend service for storing and retrieving data about important
natural sites and observations thereof. This information is structured
along the form of a database developed in the City of Helsinki during several
years. It is not particularly specific to Helsinki and should be usable
elsewhere as well.

Data in LTJ is accessed throught its ReST-like API. In addition there is a
reasonably functional admnistration site implemented using Django admin.
In case you are not familiar with Django admin, it is a simple forms based
editor of Web 1.0 style.

LTJ also has support for displaying HTML-formatted reports for natural
sites. These are designed for linking from the Helsinki map service
(kartta.hel.fi).
 
## Installation

This applies to both development and simple production scale (nature
information is, sadly, not very popular). Note that you won't need to
follow this approach if you have your own favorite Python process.

### Prerequisites

* Python 3
* PostgreSQL with PostGIS (other databases are not tested at all)

### Configuration

LTJ uses environment variables for its configuration. These are particularly
nice in container environments or other managed environments (like Heroku).

However for development, setting the environment variables is a bit
annoying. In this case you will want to create `config.env` in the root
of the source (ie. same place as this README). Start by renaming
`config.env.example` to `config.env`. The example file should
contain every setting currently available and commonly used
values thereof.

### Preparing the database

LTJ uses PostGIS for storing the geometries (areas on map) and/or points
(locations on map) of natural phenomena. Therefore you need to have the
PostGIS extension installed and enable for the database.

Begin by adding enabling PostGIS extension for the default template;

    sudo -u postgres psql -d template1 -c "CREATE EXTENSION IF NOT EXISTS postgis;"

Create user and database

    sudo -u postgres createuser -P -R -S ltj  # use password `ltj`
    sudo -u postgres createdb -O ltj ltj
   
Allow user to create test database

    sudo -u postgres psql -c "ALTER USER ltj CREATEDB;"
    
The application is build based on existing database, import data from a dump (
note that it should be fresh dump from original database without any migration
being applied on nature model):

    psql -h localhost -p 5432 -U ltj ltj < data_dump.sql
    
Run the utility script to fix the database so that it can be managed by django:

    psql -h localhost -U ltj -d ltj -a -f utility/add_alter_columns.sql
    psql -h localhost -U ltj -d ltj -a -f utility/add_id_seq.sql
    psql -h localhost -U ltj -d ltj -a -f utility/protection_level_comments.sql  # optional

    # convert columns with type `timestamp without time zone` to type `timestamp with time zone`
    psql -h localhost -U ltj -d ltj -a -f utility/drop_views.sql -f utility/tz_aware_timestamps.sql -f utility/create_views.sql

Fake initial when first time run migrations on nature app:
    
    python manage.py migrate nature --fake-initial

If migrations change the columns that are used by views, drop views before applying migrations and recreate after it.

    psql -h localhost -U ltj -d ltj -a -f utility/drop_views.sql
    python manage.py migrate
    psql -h localhost -U ltj -d ltj -a -f utility/create_views.sql

### Tests

Run tests

    py.test

Run tests with coverage report

    py.test --cov-report html --cov .
    
Open htmlcov/index.html for the coverage report.


### Translations

To compile the Finnish translations run

    python manage.py compilemessages
