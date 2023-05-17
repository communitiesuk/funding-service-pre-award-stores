# funding-service-design-fund-store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design fund store.

Built with Flask.

## Prerequisites
- python ^= 3.10

# Getting started

## Installation

Clone the repository.

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

NOTE: requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run:

    pip-compile requirements.in

    pip-compile requirements-dev.in

## How to use
Enter the virtual environment as described above, then:

    flask run

### Run with Gunicorn

In deployed environments the service is run with gunicorn. You can run the service locally with gunicorn to test

First set the FLASK_ENV environment you wish to test eg:

    export FLASK_ENV=dev

Then run gunicorn using the following command:

    gunicorn wsgi:app -c run/gunicorn/local.py

# Pipelines

Place brief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.

# Testing

## Unit

To run all tests in a development environment run:

    pytest

# Extras

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.

In deploy.yml, there are three environment variables called users, spawn-rate and run-time. These are used
to override the locust config if the performance tests need to run with different configs for fund store.

# Data
This repo also defines the production data for funds and rounds in JSON format in lieu of a real database. Certain fields can be overridden through environment variables in the following format:

        force_fieldname_roundshortid=value

The fields that can be overridden are: opens, deadline, assessment_deadline. So to override the opening date:

        export force_opens_R2W3=2023-01-01

You can also force all defined rounds to be open by setting the environment variable `FORCE_OPEN`. This has the effect of setting the following values for all rounds:

        `opens = "2022-02-02 12:00:00",
        deadline = "2024-12-31 11:59:00",`

# Seeding Fund Data
To seed fund & round data to db

```
docker exec -ti <fund_store_container_id> scripts/load_cof_r2.py

```
```
docker exec -ti <fund_store_container_id> scripts/load_cof_r3w1.py

```
To amend the round dates
```
docker exec -ti <fund_store_container_id> scripts/amend_round_dates.py --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --assessment_deadline_date "2023-03-30 12:00:00"

```
```
docker exec -ti <fund_store_container_id> scripts/amend_round_dates.py --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --opens_date "2022-10-04 12:00:00" --deadline_date "2022-12-14 11:59:00" --assessment_deadline_date "2023-03-30 12:00:00"

```