"""..

include:: ./README.md
"""
from invoke import task
from tasks.db_tasks import bootstrap_dev_db
from tasks.db_tasks import create_seeded_db
from tasks.db_tasks import generate_test_data
from tasks.db_tasks import seed_dev_db
from tasks.helper_tasks import profile_pytest
from tasks.helper_tasks import reqs

task.auto_dash_names = False

__all__ = [
    seed_dev_db,
    create_seeded_db,
    bootstrap_dev_db,
    profile_pytest,
    reqs,
    generate_test_data,
]
