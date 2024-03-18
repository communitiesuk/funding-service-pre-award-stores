# funding-service-design-fund-store

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is the fund store for funding service design Access Funding. This service provides an API and associated model implementation for fund and round configuration data.

[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md)

This service depends on:
- A postgres database
- No other microservices

# Data
## Local DB Setup
General instructions for local db development are available here: [Local database development](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)

## DB Helper Scripts
This repository uses `invoke` to provide scripts for dropping and recreating the local database in [tasks.py](./tasks.py)

### Running Locally

To run locally, make sure `psql` client is installed on your machine(https://www.postgresql.org/download/) and set the environment variable `DATABASE_URL`,
```bash
# pragma: allowlist nextline secret
export DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/fund_store
```

### Running in-container
To run the tasks inside the docker container used by docker compose, first bash into the container:
```bash
docker exec -it $(docker ps -qf "name=fund-store") bash
```
Then execute the required tasks using `inv` as below.

Or to combine the two into one command:
```bash
    docker exec -it $(docker ps -qf "name=fund-store") inv truncate-data
```

### Available scripts
The following commands are the same locally or in container

### Recreate DB instance

        inv recreate-local-db

this drops (if it exists) and recreates the DB

### Truncate data

        inv truncate-data
)

## Seeding Fund Data
To seed fund & round data to db for all funds and rounds, use the fund/round loaders scripts.

If running against a local postgresql instance:
```bash
    python -m scripts.load_all_fund_rounds
```

If running with the docker compose setup:

```bash
    docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.load_all_fund_rounds
```

Further details on the fund/round loader scripts, and how to load data for a specific fund or round can be found [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/40337455/Adding+or+updating+fund+and+round+data)

## Amending round dates
This script allows you to open/close rounds using their dates to test different functionality as needed. You can also use the keywords 'PAST', 'FUTURE' and 'UNCHANGED' to save typing dates.

```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q update-round-dates --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --application_deadline "2023-03-30 12:00:00"

docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q update-round-dates -r COF_R3W3 -o "2022-10-04 12:00:00" -d "2022-12-14 11:59:00" -ad "2023-03-30 12:00:00" -as NONE

docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q update-round-dates -r COF_R3W3 -o PAST -d FUTURE
```
For an interactive prompt where you can supply (or leave unchanged) all dates:
```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates update-round-dates
```
To reset the dates for a round to those in the fund loader config:
```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates -q reset-round-dates -r COF_R4W1
```
And with an interactive prompt:
```bash
docker exec -ti $(docker ps -qf "name=fund-store") python -m scripts.amend_round_dates reset-round-dates
```

# Testing
[Testing in Python repos](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)


# IDE Setup
[Python IDE Setup](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md)


# Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)
## Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)
## Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the fund store:
- service-name: fsd-fund-store
- image-name: funding-service-design-fund-store
