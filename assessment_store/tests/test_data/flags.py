import datetime

from db.models.flags.enums import FlagType

now = datetime.datetime.now()
earlier = now - datetime.timedelta(days=1)

flag_config = [
    {
        "flag_type": FlagType.STOPPED,
        "justification": "Test justification 2",
        "sections_to_flag": ["Test section 2"],
        "date_created": earlier,
        "user_id": "user2",
    },
    {
        "flag_type": FlagType.FLAGGED,
        "justification": "Latest 1",
        "sections_to_flag": ["Test section 1"],
        "date_created": now,
        "user_id": "user1",
    },
    {
        "flag_type": FlagType.QA_COMPLETED,
        "justification": "Test justification 3",
        "sections_to_flag": ["Test section 3"],
        "date_created": earlier,
        "user_id": "user3",
    },
    {
        "flag_type": FlagType.FLAGGED,
        "justification": "Latest 2",
        "sections_to_flag": ["Test section 3"],
        "date_created": now,
        "user_id": "user3",
    },
    {
        "flag_type": FlagType.QA_COMPLETED,
        "justification": "Test justification 4",
        "sections_to_flag": ["Test section 4"],
        "date_created": earlier,
        "user_id": "user4",
    },
    {
        "flag_type": FlagType.QA_COMPLETED,
        "justification": "Latest 3",
        "sections_to_flag": ["Test section 4"],
        "date_created": now,
        "user_id": "user4",
    },
]
