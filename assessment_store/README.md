# Funding Service Design - Assessment Store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![Funding Service Design Assessment Store Deploy](https://github.com/communitiesuk/funding-service-design-assessment-store/actions/workflows/deploy.yml/badge.svg)
[![CodeQL](https://github.com/communitiesuk/funding-service-design-assessment-store/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/communitiesuk/funding-service-design-assessment-store/actions/workflows/codeql-analysis.yml)

Repo for the DLUHC Funding Service Design Assessment Store.

Built with Flask.

## Prerequisites
- python ^= 3.10
- postgres or (docker if running postgres in docker).

# Getting started

## Quickstart / TL;DR
If on windows: use `python` instead of `python3`, `set` instead of `export`, and `.venv\Scripts\activate` instead of `.venv/bin/activate`.

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
docker container run -e POSTGRES_PASSWORD=postgres -p 5432:5432 --name=assess_store_postgres -e POSTGRES_DB=assess_store_dev postgres
export DATABASE_URL='postgresql://postgres:postgres@127.0.0.1:5432/assess_store_dev'
flask run
```

## Installation

- Clone the repository

### Create a Virtual environment

    python3 -m venv .venv

### Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt

NOTE: The psycopg2 package (required for PostgreSQL) can sometimes have difficulty installing on certain environments
related to libssl.
If you experience difficulties on macOS this might be required:

    export LDFLAGS="-L/usr/local/opt/openssl/lib"

or see other resolutions on [StackOverflow](https://stackoverflow.com/questions/11365619/psycopg2-installation-error-library-not-loaded-libssl-dylib)

To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run:

    pip-compile requirements.in

    pip-compile requirements-dev.in

### Setting up for database development
This service is designed to use PostgreSQL as a database, via SqlAlchemy
When running the service (eg. `flask run`) you need to set the DATABASE_URL environment variable to the URL of the database you want to test with.

Initialise the database:

    flask db init

Then run existing migrations:

    flask db upgrade

Whenever you make changes to database models, please run:

    flask db migrate

This will create the migration files for your changes in /db/migrations.
Please then commit and push these to github so that the migrations will be run in the pipelines to correctly
upgrade the deployed db instances with your changes.

## How to use
Enter the virtual environment and setup the db as described above, then:
## How to run locally
Enter the virtual environment and install dependencies as described above, then:

### Create and seed local DB
- Make sure your local `DATABASE_URL` env var is set to your local postgres db (this doesn't need to actually exist yet), eg:

        DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/fsd_assess_store

- Use `tasks\db_tasks.py` to create and seed this DB (follow command prompts for what data to create):

        invoke create_seeded_db

### Run Flask

Run:

    flask run

A local dev server will be created on

    http://localhost:5000

Flask environment variables are configurable in `.flaskenv`

### Run with Gunicorn

In deployed environments the service is run with gunicorn. You can run the service locally with gunicorn to test

First set the FLASK_ENV environment you wish to test eg:

    export FLASK_ENV=dev

Then run gunicorn using the following command:

    gunicorn wsgi:app -c run/gunicorn/local.py

# Configuration

# Pipelines

These are the current pipelines running on the repo:

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.
* NOTE: THIS IS A CUSTOM DEPLOY WORKFLOW AND DOES NOT YET USE THE WORKFLOW TEMPLATE FOR FUNDING SERVICE DESIGN PENDING UPDATE

# Testing

The tests within /tests are designed to connect to a real database to run tests that use the DB layer, details below. This takes a long time to setup on a test run, so if your tests don't need a DB put them in /tests_no_db. This folder doesn't pickup /tests/conftest.py so therefore doesn't do the DB setup work and these tests can run in isolation much faster.

## Seed Postgres DB with mock data

`invoke seed_dev_db`

Running the above command will prompt you to enter the number of applications, funds & rounds you would like to create as mock data within the database.

This will also work for the DB within the docker runner. Find the ID of the docker container running assessment-store (`docker ps`) then execute:

        docker exec -it <container_id> invoke seed_dev_db

To avoid the interactive prompt, alternatively the fund-round and application count can be provided as arguments
such as: 

        invoke seed_dev_db --fundround COFR2W2 --appcount 1

## Unit & Accessibility Testing

1. Ensure you have a local postgres instance setup and running with a user `postgres` created.
2. Ensure that you have set a DATABASE_URL environment variable.
3. Install `requirements-dev.txt`
4. Activate your virtual env: `source .venv/bin/activate`
5. Run pytest

NB : pytest will create a database with a unique name to use just for unit tests. Changes to this db from tests does not persist. Caching is enable so that sequential pytest invocations will reuse the database with the test data. **Again, only the seeded data is reused since changes due to unit tests are not persisted.**

To rerun the unit test database creation/seeding process run `pytest --cache-clear`. This is the same as deleting the `.pytest_cache` directory.

If you have deleted the unit test database and then get errors where no rows exist, you need to clear the cache as above before running the unit tests again.

## Transactional tests
These rely on the module `pytest-flask-sqlalchemy` which has good docs on its github page: https://github.com/jeancochrane/pytest-flask-sqlalchemy

The main parts of this framework are invoked in `conftest.py` with the following fixture definitions:
- `enable_transactional_tests` - This makes all tests use transactions so we don't need to turn it on for each test individually
- `_db` - this makes the framework use our `db` variable from `db.db`, overriding anywhere it is used during the tests.

`conftest.py` also seeds data into the test db which enables all the tests to be run individually - no test should rely on another to run before or after it. This seeded data is also rolled back after a test session.

To make the tests work with a test postgres db in the github pipelines, we pass the following 2 inputs to the shared workflow:

      postgres_unit_testing: true
      db_name: fsd_assess_store_test

## Performance Testing

Performance tests are stored in a separate repository which is then run in the pipeline. If you want to run the performance tests yourself follow the steps in the README for the performance test repo located [here](https://github.com/communitiesuk/funding-service-design-performance-tests/blob/main/README.md)

## Testing FAQS

### Q: help! My tests are failing because of `no rows found`
You've deleted your unit test db or done something manually, so pytest's cache is confused.
Run `pytest --cache-clear` to fix your problem.


# Extras

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual environment:

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.

# Database on Paas
Create db service with:

    cf create-service postgres medium-13 assessment-store-dev-db

Ensure the following elements are present in your `manifest.yml`. The `run_migrations_paas.py` is what initialises the database, and the `services` element binds the application to the database service.

    command: scripts/run_migrations_paas.py && gunicorn wsgi:app -c run/gunicorn/devtest.py

    services:
        - assessment-store-dev-db
