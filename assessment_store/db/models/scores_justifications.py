import uuid
from datetime import datetime

from db import db


class ScoresJustifications(db.Model):
    scores_justifications_id = db.Column(
        "scores_justifications_id",
        db.Text(),
        default=lambda: uuid.uuid4(),
        primary_key=True,
    )
    timestamp = db.Column("timestamp", db.Text(), default=str(datetime.now()))
    assessment_id = db.Column(
        "assessment_id",
        db.Text(),
        ForeignKey=True,
    )
    person_id = db.Column(
        "person_id",
        db.Text(),
        ForeignKey=True,
    )
    sub_criteria_id = db.Column(
        "sub_criteria_id",
        db.Text(),
        ForeignKey=True,
    )
    score = db.Column(
        db.Integer(),
    )
    justification = db.Column(
        db.Text(),
    )

    def __repr__(self):
        return f"<Sub-Criteria {self.sub_criteria_title}, {self.sub_criteria_id} \
                for Criteria {self.criteria_id} \
                of Round {self.round_id}>"

    def as_json(self):
        return {
            "sub_criteria_id": self.sub_criteria_id,
            "round_id": self.round_id,
            "criteria_id": self.criteria_id,
            "sub_criteria_title": self.sub_criteria_title,
        }


class ScoresJustificationsError(Exception):
    """Exception raised for errors in Sub-Criteria management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class ScoresJustificationsMethods:
    @staticmethod
    def score_justification(as_json=False):
        scores_justifications = ScoresJustifications.query.all()
        if as_json:
            return [record.as_json() for record in scores_justifications]
        return scores_justifications

    @staticmethod
    def get_by_id(scores_justifications_id: str):
        score_justification = ScoresJustifications.query.get(
            scores_justifications_id
        )
        if not score_justification:
            raise ScoresJustifications(
                message="Sub-Criteria could not be found"
            )
        return score_justification
