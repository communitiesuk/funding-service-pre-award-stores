import datetime

from db.models.flags.enums import FlagType

now = datetime.datetime.now()
earlier = now - datetime.timedelta(days=1)

flag_config = [
    {
        "application_id": "a3ec41db-3eac-4220-90db-c92dea049c00",
        "flag_type": FlagType.STOPPED,
        "justification": "Test justification 2",
        "section_to_flag": "Test section 2",
        "date_created": earlier,
        "user_id": "user2",
    },
    {
        "application_id": "a3ec41db-3eac-4220-90db-c92dea049c00",
        "flag_type": FlagType.FLAGGED,
        "justification": "Latest 1",
        "section_to_flag": "Test section 1",
        "date_created": now,
        "user_id": "user1",
    },
    {
        "application_id": "a3ec41db-3eac-4220-90db-c92dea049c01",
        "flag_type": FlagType.QA_COMPLETED,
        "justification": "Test justification 3",
        "section_to_flag": "Test section 3",
        "date_created": earlier,
        "user_id": "user3",
    },
    {
        "application_id": "a3ec41db-3eac-4220-90db-c92dea049c01",
        "flag_type": FlagType.FLAGGED,
        "justification": "Latest 2",
        "section_to_flag": "Test section 3",
        "date_created": now,
        "user_id": "user3",
    },
    {
        "application_id": "c3ec41db-3eac-4220-90db-c92dea049c03",
        "flag_type": FlagType.QA_COMPLETED,
        "justification": "Test justification 4",
        "section_to_flag": "Test section 4",
        "date_created": earlier,
        "user_id": "user4",
    },
    {
        "application_id": "c3ec41db-3eac-4220-90db-c92dea049c03",
        "flag_type": FlagType.QA_COMPLETED,
        "justification": "Latest 3",
        "section_to_flag": "Test section 4",
        "date_created": now,
        "user_id": "user4",
    },
]
