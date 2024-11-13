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
- No other microservices

### IDE Setup
[Python IDE Setup](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md)

### Setup pre-commit checks

* [Install pre-commit locally](https://pre-commit.com/#installation)
* Pre-commit hooks can either be installed using pip `pip install pre-commit` or homebrew (for Mac users) `brew install pre-commit`
* From your checkout directory run `pre-commit install` to set up the git hook scripts


## Data

### Local DB Setup
General instructions for local db development are available here: [Local database development](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)

### DB Helper Scripts
This repository uses `invoke` to provide scripts for dropping and recreating the local database in [tasks.py](./tasks.py)

### Running in-container
To run the tasks inside the docker container used by docker compose, first bash into the container:
```bash
docker exec -it $(docker ps -qf "name=pre-award-stores") bash
```
Then execute the required tasks using `inv` as below.

Or to combine the two into one command:
```bash
docker exec -it $(docker ps -qf "name=pre-award-stores") inv truncate-data
```

## Running the tests

We use `pytest` to run all of our tests. We have a selection of unit, integration, and end-to-end (browser) tests. By default,
the unit and integration tests will run with a basic invocation of `pytest.`

The majority of our tests will expect to access a database. This will be available if you're using the docker runner and have started all of the services.

[Testing in Python repos](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)

## Updating database migrations

Whenever you make changes to database models, please run:

`uv run flask db migrate -m <message>`

The `message` should be a short description of the DB changes made. Don't specify a revision id (using `--rev-id`) - it will be generated automatically.

The migration file for your changes will be created in ./db/migrations. Please then commit and push these to github
so that the migrations will be run in the pipelines to correctly upgrade the deployed db instances with your changes.


## Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)
### Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)
### Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the fund store:
- service-name: pre-award-stores
- image-name: ???

## Accessing on AWS

TODO: Some AWS access info
