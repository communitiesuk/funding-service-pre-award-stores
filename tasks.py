from invoke import Collection

from account_store import tasks as account_tasks
from assessment_store import tasks as assessment_tasks

namespace = Collection()
namespace.add_collection(Collection.from_module(assessment_tasks), "assessment")
namespace.add_collection(Collection.from_module(account_tasks), "account")
