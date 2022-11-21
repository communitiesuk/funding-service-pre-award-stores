"""
.. include:: ./README.md
"""
import inspect

from tasks.db_tasks import bootstrap_dev_db
from tasks.db_tasks import create_seeded_db
from tasks.db_tasks import seed_dev_db
from tasks.helper_tasks import profile_pytest
from tasks.helper_tasks import reqs

__all__ = [
    seed_dev_db,
    create_seeded_db,
    bootstrap_dev_db,
    profile_pytest,
    reqs,
]

# Needed for invoke to work on python3.11
# Remove once invoke has been updated.
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec
