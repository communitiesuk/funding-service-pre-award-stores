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
## Import submitted applications from application_store
To import the submitted applications of a round into assessment, execute the below command.

    docker exec -it <container_id> python -m scripts.import_from_application --roundid=c603d114-5364-4474-a0c4-c41cbf4d3bbd --app_type=COF
or with short name set `--use_short_name=True`

    docker exec -it <container_id> python -m scripts.import_from_application --roundid=COFR3W1 --use_short_name=True

If using VsCode, select the launch config "[Import Applications to Assessment](#launch-config-vscode)" to import the application.


## Seed Postgres DB with mock data

`invoke seed_dev_db`

Running the above command will prompt you to enter the number of applications, funds & rounds you would like to create as mock data within the database.

This will also work for the DB within the docker runner. Find the ID of the docker container running assessment-store (`docker ps`) then execute:

        docker exec -it <container_id> invoke seed_dev_db

To avoid the interactive prompt, alternatively the fund-round and application count can be provided as arguments
such as:

        invoke seed_dev_db --fundround COFR2W2 --appcount 1

If using VsCode, select the launch config "[Seed Applications in assessment-store](#launch-config-vscode)" to start seeding.

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

Test data is created on a per-test basis to prevent test pollution. To create test data for a test, request the `seed_application_records` fixture in your test. That fixture then provides access to the inserted records and will clean up after itself at the end of the test session.

More details on the fixtures in utils: https://github.com/communitiesuk/funding-service-design-utils/blob/dcc64b0b253a1056ce99e8fe7ea8530406355c96/README.md#fixtures

Basic example:

    @pytest.mark.apps_to_insert(
        [
            {
                # Assessment_Records data
                # For convencience a set of these are loaded into the variable test_input_data in conftest.py
                test_input_data[0]
            }
        ]
    )
    def test_stuff(seed_application_records):
      app_id = seed_application_records[0].id
      # do some testing

## Flags
If you need your test assessment records to be flagged, you can supply flag config as part of the apps_to_insert data by including
an array of flag configs under the property `flags`. Some example flag configs are contained in test_data/flags.py


    @pytest.mark.apps_to_insert(
        [
            test_input_data[0],
            {**test_input_data[1], "flags": [flag_config[2]]},
            {**test_input_data[2], "flags": [flag_config[1]]},
        ]
    )
    def test_stuff(seed_application_records):
        flag = retrieve_flag_for_application(seed_application_records[1].id)
        assert flag == flag_config[2]

## Unique Fund and Round IDs - same for all applications
If you need all your test data to use the same fund and round ids, but be different from all other tests, use `unique_fund_round` in your test. This generates a random ID for fund and round and uses this when creating test applications.

    pytest.mark.apps_to_insert([test_input_data[0]])
    @pytest.mark.unique_fund_round(True)
    def test_some_reports(
        seed_application_records
    ):
        result = get_by_fund_round(
            fund_id=seed_application_records[0]["fund_id"], round_id=seed_application_records[0]["round_id"]
        )

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

# Launch Configurations in VsCode
<a id="launch-config-vscode"></a>
If you are using VsCode, we have prepared frequently used scripts in the launch configuration that can be handy for quick development. Below are some launch configurations that you will find in the `launch.json` file.

*Import Applications to Assessment* - import applications for the provided round from application_store to assessment_store. Please provide the `--roundid` & `--app_type` in the arguments as shown below.
 ```
 {
    "name": "Import Applications to Assessment",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/scripts/import_from_application.py",
    .
    .
    .
    // modify the args accordingly
    "args": ["--roundid", "fc7aa604-989e-4364-98a7-d1234271435a",
    "--app_type", "NSTF"]
  },
 ```

*Seed Applications in assessment-store* - Creates the mock assessments data for the provided round in interactive prompt.
 ```
 {
    "name": "Seed Applications in assessment-store",
    "type": "python",
    "request": "launch",
    .
    .
    .
    "justMyCode": false,
    "args": ["seed_dev_db"]
},
 ```

*Feed location in assessment-store* - Populates the location data in the assessment records for the provided round.
Please provide the `--fund_id`, `--round_id` and any additional arguments as shown below.
 ```
  {
    "name": "Feed location in assessment-store",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/scripts/populate_location_data.py",
    .
    .
    .
    // modify the args accordingly
    "args": ["--fund_id", "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
      "--round_id", "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
      "--update_db", "True",
      "--write_csv", "False"]
  },
 ```
