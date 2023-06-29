import datetime
from uuid import uuid4

from db.models.flags.enums import FlagType
from db.models.flags_v2.flag_update import FlagStatus

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

user_id = uuid4()
flag_config_v2 = [
    {
        "status": FlagStatus.RAISED,
        "justification": "Test justification 2",
        "sections_to_flag": ["Test section 2"],
        "date_created": earlier,
        "user_id": user_id,
        "allocation": "TEAM_1",
    },
]

add_flag_update_request_json = {
    "user_id": str(user_id),
    "status": FlagStatus.STOPPED,
    "allocation": "TEAM_2",
    "justification": "stopping assessment",
}

create_flag_request_json = {
    "justification": "some text",
    "status": FlagStatus.RAISED,
    "allocation": "TEAM_1",
    "sections_to_flag": ["section_1"],
    "user_id": str(user_id),
}
