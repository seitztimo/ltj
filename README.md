[![Build status](https://travis-ci.org/City-of-Helsinki/ltj.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/ltj)
[![codecov](https://codecov.io/gh/City-of-Helsinki/ltj/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/ltj)
[![Requirements](https://requires.io/github/City-of-Helsinki/ltj/requirements.svg?branch=master)](https://requires.io/github/City-of-Helsinki/ltj/requirements/?branch=master)

# ltj
City of Helsinki nature database and API


## Development

### Database

Adding postgis extention to default template;

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
    
### Tests

Run tests

    py.test

Run tests with coverage report

    py.test --cov-report html --cov .
    
Open htmlcov/index.html for the coverage report.


## Translations

To compile the Finnish translations run

    python manage.py compilemessages
