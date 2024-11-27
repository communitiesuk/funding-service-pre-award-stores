# funding-service-pre-award-stores

A repository for the combined pre-award stores (currently empty, but will eventually encompass Fund, Application and Assessment stores).


## Setup

The recommended and supported way of running this service is using [the docker runner](https://github.com/communitiesuk/funding-service-design-docker-runner/). Please see that repository for instructions on running using `docker-compose`.

You will likely still want to create a local virtual environment for python dependencies, but you should only run the application using the provided docker-compose file.

We use [uv](https://docs.astral.sh/uv/) to manage Python versions and local virtual environments.

```bash
uv sync
```

To update requirements, use `uv add` or `uv remove`.

### Setup guide

[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md)

This service depends on:
- A postgres database

### IDE Setup
[Python IDE Setup](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md)

### Setup pre-commit checks

* [Install pre-commit locally](https://pre-commit.com/#installation)
* Pre-commit hooks can either be installed using pip `pip install pre-commit` or homebrew (for Mac users) `brew install pre-commit`
* From your checkout directory run `pre-commit install` to set up the git hook scripts


## Data

### Local DB Setup
General instructions for local db development are available here: [Local database development](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)

## Updating database migrations

Whenever you make changes to database models, please run:

`uv run flask db migrate -m <message>`

The `message` should be a short description of the DB changes made. Don't specify a revision id (using `--rev-id`) - it will be generated automatically.

The migration file for your changes will be created in ./db/migrations/versions. Please then commit and push these to github
so that the migrations will be run in the pipelines to correctly upgrade the deployed db instances with your changes.

## Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)
### Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)

### Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the fund store:
- service-name: fsd-pre-award-stores

# Fund Store Specifics


## Seeding Fund Data
To seed fund & round data to db for all funds and rounds, use the fund/round loaders scripts.

If running against a local postgresql instance:
```bash
    python -m fund_store.scripts.load_all_fund_rounds
```

Further details on the fund/round loader scripts, and how to load data for a specific fund or round can be found [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/40337455/Adding+or+updating+fund+and+round+data)

## Amending round dates
This script allows you to open/close rounds using their dates to test different functionality as needed. You can also use the keywords 'PAST', 'FUTURE' and 'UNCHANGED' to save typing dates.

```bash
docker exec -ti $(docker ps -qf "name=pre-award-stores") python -m fund_store.scripts.amend_round_dates -q update-round-dates --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --application_deadline "2023-03-30 12:00:00"

docker exec -ti $(docker ps -qf "name=pre-award-stores") python -m fund_store.scripts.amend_round_dates -q update-round-dates -r COF_R3W3 -o "2022-10-04 12:00:00" -d "2022-12-14 11:59:00" -ad "2023-03-30 12:00:00" -as NONE

docker exec -ti $(docker ps -qf "name=pre-award-stores") python -m fund_store.scripts.amend_round_dates -q update-round-dates -r COF_R3W3 -o PAST -d FUTURE
```
For an interactive prompt where you can supply (or leave unchanged) all dates:
```bash
docker exec -ti $(docker ps -qf "name=pre-award-stores") python -m fund_store.scripts.amend_round_dates update-round-dates
```
To reset the dates for a round to those in the fund loader config:
```bash
docker exec -ti $(docker ps -qf "name=pre-award-stores") python -m fund_store.scripts.amend_round_dates -q reset-round-dates -r COF_R4W1
```
And with an interactive prompt:
```bash
docker exec -ti $(docker ps -qf "name=pre-award-stores") python -m fund_store.scripts.amend_round_dates reset-round-dates
```

# Application Store Specifics


## Simple Queue Service
As part of the application submission workflow, we use a [FIFO AWS SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html) to automate our application export to assessment.

We export the application as a 'fat' payload. This includes all application data (including metadata/attributes), this ensure assessment does not need to call application_store for additional information.

We can simulate an SQS locally when using our docker runner instance. Our docker runner uses localstack to simulate these  AWS services, see [here](https://github.com/communitiesuk/funding-service-design-docker-runner/tree/main/docker-localstack).

If messages are not consumed and deleted they will be move to the Dead-Letter_Queue, here we can inspect the message for faults and retry.

The SQS queues have a number of confiuration options, we are using the AWS SDK for Python (Boto3), see docs [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html).

There is an API endpoint on this service to send a submitted application to assessment:

```
/queue/{queue_name}/{application_id}
```


## Seeding Test Data
You can seed test data to use in the running application (separate to unit test data seeding). The seeding process needs a running fund-store to retrieve fund/round form section config, so it runs within the docker container for application-store within the docker runner.
To run the seeding script:
1. Make sure your local docker-runner is running
1. Find the container ID of `pre-award-stores` by using `docker ps`
1. Use docker exec to get into that container: `docker exec -it <container_id> bash`
1. Execute the script: `python application_store/scripts/seed_db_test_data.py`. You will be prompted for inputs: fund, round, account_id (the UUID not email address), the status of the seeded applications and how many to create.

### Testing the seeding process
Unit tests exist in [test_seed_db](/tests/application_store_tests/test_seed_db.py). They are marked as skipped as they require a running fund-store to retrieve form config (no point in duplicating this for tests) so they won't run in the pipeline but are fine locally. If your local fund store runs on a non-standard port etc, edit the `local_fund_store` fixture in that tests file. If you want to run the tests, just comment out the skip marker.

### Adding a new fund/round to the seeding process
To seed applicaitons, we need the completed form json. If you have that, skip to the end of part 1 and put that form json into the required file.

#### Part 1 - get the form json
1. Get a submitted application into your local DB. You can either do this manually or by running the automated tests against your local docker runner.
1. Find the `application_id` of that submitted application._
1. Edit the [tests file](/tests/application_store_tests/test_seed_db.py) to un-skip `test_retrieve_test_data` and then set `target_app` to be the `application_id` you just submitted.
1. Update your unit test config to point at the same DB as the docker runner. Update [pytest.ini](/pytest.ini) so that `D:DATABASE_URL` points at the docker runner application store db: `D:DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/application_store  # pragma: allowlist secret`
1. Run the single test `test_retrieve_test_data` - this should output the json of all the completed forms for that application into funding-service-design-store/forms.json.
1. Copy this file into [seed_data](/tests/application_store_tests/seed_data/) and name it `<fund_short_code>_<round_short_code>_all_forms.json`.
1. *IMPORTANT* Change the config in [pytest.ini](/pytest.ini) back to what it was so you don't accidentally wipe your docker runner DB next time you run tests!

#### Part 2 - update seeding config
1. In [seed_db](/tests/application_store_tests/seed_data/seed_db.py) there is a constant called `FUND_CONFIG` - update this following the existing structure for your new fund/round (if it's a new round on an existing fund, just add it as another key to `rounds` item in that fund). You will need to know the name of the form that contains the field used to the name the application/project.
1. In the same file, update the `click.option` choice values for fund/round as required, to allow your new options.
1. Test it - update the unit tests to use this new config and check it works.
