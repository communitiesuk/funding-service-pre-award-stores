import uuid

from sqlalchemy import Index, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils.types import UUIDType

from db import db


class AssessmentRecords(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    application_id = db.Column(
		"application_id",
		db.Text(),
		nullable=False,
	)
		
    application_json = db.Column("application_json", JSONB)

Index(
    "application_json_index",
    AssessmentRecords.application_json,
    postgresql_ops={
        "application_json": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

def find_field_by_key(field_key: str, app_id : str):

    return (
        db.session.query(
                func.jsonb_path_query_first(
                AssessmentRecords.application_json,
                f"$[*].fields[*] ? (@.key == \"{field_key}\")",
            )
        )
        .select_from(AssessmentRecords)
        .filter(
            AssessmentRecords.application_json.contains(
                [ { "fields": [ { "key" : field_key } ] } ]
            )
        )
        .filter(AssessmentRecords.application_id == app_id)
        .one()
    )