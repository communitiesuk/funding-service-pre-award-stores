from invoke import Collection

from account_store import tasks as account_tasks
from assessment_store import tasks as assessment_tasks
from common import tasks as common_tasks

namespace = Collection()
namespace.add_collection(Collection.from_module(assessment_tasks), "assessment")
namespace.add_collection(Collection.from_module(account_tasks), "account")
namespace.add_collection(Collection.from_module(common_tasks), "common")
