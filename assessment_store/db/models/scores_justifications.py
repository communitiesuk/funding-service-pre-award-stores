import uuid
from datetime import datetime

from db import db
from db.models.assessment import Assessment
from db.models.sub_criteria import SubCriteria
from sqlalchemy import DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils.types import UUIDType


class ScoresJustifications(db.Model):
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    created_at = db.Column("created_at", DateTime(), default=datetime.utcnow)
    assessment_id = db.Column(
        "assessment_id",
        db.String(255),
        db.ForeignKey(Assessment.id),
    )
    assessor_user_id = db.Column(
        "assessor_user_id",
        db.String(255),
    )
    sub_criteria_id = db.Column(
        "sub_criteria_id",
        db.String(255),
        db.ForeignKey(SubCriteria.id),
    )
    score = db.Column(
        db.Integer(),
    )
    justification = db.Column(
        db.Text(),
    )

    def __repr__(self):
        return f"""ScoresJustifications(
                sub_criteria_id={self.sub_criteria_id},
                assessment_id={self.assessment_id},
                score={self.score},
                justification={self.justification},
                assessor_user_id={self.assessor_user_id},
            )"""

    def __str__(self):
        return f"<Score of {self.score}, justification of {self.justification} \
                for Sub-Criteria {self.sub_criteria_id} \
                of Assessment {self.assessment_id} \
                by Person {self.assessor_user_id}>"

    def as_json(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "assessment_id": self.assessment_id,
            "assessor_user_id": self.assessor_user_id,
            "sub_criteria_id": self.sub_criteria_id,
            "score": self.score,
            "justification": self.justification,
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
    def scores_justifications(
        sub_criteria_id: str, assessment_id: str, as_json=False
    ):
        scores_justifications = (
            db.session.query(ScoresJustifications)
            .filter(
                ScoresJustifications.assessment_id == assessment_id,
                ScoresJustifications.sub_criteria_id == sub_criteria_id,
            )
            .all()
        )
        if as_json:
            return [record.as_json() for record in scores_justifications]
        return scores_justifications

    @staticmethod
    def get_by_id(id: str):
        score_justification = ScoresJustifications.query.get(id)
        if not score_justification:
            raise ScoresJustifications(
                message="Sub-Criteria could not be found"
            )
        return score_justification

    @staticmethod
    def register_score_justification(
        sub_criteria_id: str,
        assessment_id: str,
        score: int,
        justification: str,
        assessor_user_id: str,
    ):
        try:
            score_justification = ScoresJustifications(
                sub_criteria_id=sub_criteria_id,
                assessment_id=assessment_id,
                score=score,
                justification=justification,
                assessor_user_id=assessor_user_id,
            )
            db.session.add(score_justification)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ScoresJustificationsError()
        return score_justification
