import uuid

from db import db
from sqlalchemy_utils.types import UUIDType


class Criteria(db.Model):

    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )

    criteria_name = db.Column(
        "name",
        db.Text(),
    )

    round_id = db.Column(
        "round_id",
        db.String(),
    )

    fund_id = db.Column("fund_id", db.String())

    def as_json(self):
        return {
            "round_id": self.round_id,
            "criteria_id": str(self.criteria_id),
            "criteria_name": self.criteria_name,
        }

    @property
    def uuid(self):
        return self.criteria_id
