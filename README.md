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
