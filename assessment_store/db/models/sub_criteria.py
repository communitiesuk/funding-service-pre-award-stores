import uuid

from db import db
from sqlalchemy_utils.types import UUIDType


class SubCriteria(db.Model):
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    round_id = db.Column(
        "round_id",
        db.String(255),
    )
    criteria_id = db.Column(
        "criteria_id",
        db.String(255),
    )
    sub_criteria_title = db.Column(
        db.Text(),
    )

    def __repr__(self):
        return f"<Sub-Criteria {self.sub_criteria_title}, {self.id} \
                for Criteria {self.criteria_id} \
                of Round {self.round_id}>"

    def as_json(self):
        return {
            "id": self.id,
            "round_id": self.round_id,
            "criteria_id": self.criteria_id,
            "sub_criteria_title": self.sub_criteria_title,
        }


class SubCriteriaError(Exception):
    """Exception raised for errors in Sub-Criteria management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class SubCriteriaMethods:
    @staticmethod
    def subcriterias(as_json=False):
        subcriterias = SubCriteria.query.all()
        if as_json:
            return [subcriteria.as_json() for subcriteria in subcriterias]
        return subcriterias

    @staticmethod
    def get_by_id(id: str):
        subcriteria = SubCriteria.query.get(id)
        if not subcriteria:
            raise SubCriteriaError(message="Sub-Criteria could not be found")
        return subcriteria
