> [!IMPORTANT]
> This repository has been integrated with a new combined [pre-award-stores](https://github.com/communitiesuk/funding-service-pre-award-stores/).

# Funding Service Design - Assessment Store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![Funding Service Design Assessment Store Deploy](https://github.com/communitiesuk/funding-service-design-assessment-store/actions/workflows/deploy.yml/badge.svg)
[![CodeQL](https://github.com/communitiesuk/funding-service-design-assessment-store/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/communitiesuk/funding-service-design-assessment-store/actions/workflows/codeql-analysis.yml)

This repository offers an API and corresponding model implementation for streamlined storage and retrieval of assessment-related data, covering aspects like tagging, scoring, flagging, and sub-criteria.

[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md)

This service depends on:
- A postgres database
- [Account Store](https://github.com/communitiesuk/funding-service-design-account-store)
- [Application Store](https://github.com/communitiesuk/funding-service-design-application-store)
- [Fund Store](https://github.com/communitiesuk/funding-service-design-fund-store)
- SQS Queue

# IDE Setup
[Python IDE Setup](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md)

# Data
## Local DB Setup
General instructions for local db development are available here: [Local database development](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)

## DB Helper Scripts
This repository uses `invoke` to provide scripts for creating and seeding the local database in [tasks](tasks\TASKS.md)


# Testing
## Import submitted applications from application_store
To import the submitted applications of a round into assessment, execute the below command.

    docker exec -it <container_id> python -m scripts.import_from_application --roundid=c603d114-5364-4474-a0c4-c41cbf4d3bbd --app_type=COF
or with short name

    docker exec -it <container_id> python -m scripts.import_from_application --fundround=COFR3W1

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

NB : pytest will create a database with a unique name to use just for unit tests. Changes to this db from tests does not persist. Caching is enabled so that sequential pytest invocations will reuse the database with the test data. **Again, only the seeded data is reused since changes due to unit tests are not persisted.**

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



## Testing FAQS

### Q: help! My tests are failing because of `no rows found`
You've deleted your unit test db or done something manually, so pytest's cache is confused.
Run `pytest --cache-clear` to fix your problem.

# Launch Configurations in VsCode
If you are using VsCode, we have prepared frequently used scripts in the launch configuration that can be handy for quick development. Below are some launch configurations that you will find in the `launch.json` file.

## Import Applications to Assessment
Import applications for the provided round from application_store to assessment_store. Please provide the `--roundid` & `--app_type` in the arguments as shown below.
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
    "args": ["--fundround", "COFR3W1"]
  },
 ```

## Seed Applications in assessment-store
Creates the mock assessments data for the provided round in interactive prompt.
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
    "args": ["--fundround", "NSTFR2",
      "--update_db", "True",
      "--write_csv", "False"]
  },
 ```

# Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)

## Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)

`envs` needs to include values for each of (set with `--env <varname>=<value>`):
APPLICATION_STORE_API_HOST
SENTRY_DSN
GITHUB_SHA
DATABASE_URL

## Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the assessment store:
- service-name: fsd-assessment-store
- image-name: funding-service-design-assessment-store
