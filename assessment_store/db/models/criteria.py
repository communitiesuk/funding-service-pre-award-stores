import uuid

from db import db
from sqlalchemy_utils.types import UUIDType


class Criteria(db.Model):

    criteria_id = db.Column(
        "criteria_id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )

    criteria_name = db.Column(
        "criteria_name",
        db.Text(),
    )

    round_id = db.Column(
        "round_id",
        db.Text(),
    )

    def as_json(self):
        return {
            "round_id": self.round_id,
            "criteria_id": str(self.criteria_id),
            "criteria_name": self.criteria_name,
        }

    @property
    def uuid(self):
        return self.criteria_id
