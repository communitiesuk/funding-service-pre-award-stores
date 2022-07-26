import uuid
from datetime import datetime

from db import db
from db.models.assessment import Assessment
from db.models.sub_criteria import SubCriteria
from sqlalchemy import DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils.types import UUIDType


class Compliance(db.Model):
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    created_at = db.Column("created_at", DateTime(), default=datetime.utcnow())
    assessment_id = db.Column(
        "assessment_id",
        UUIDType(binary=False),
        db.ForeignKey(Assessment.id),
    )
    sub_criteria_id = db.Column(
        "sub_criteria_id",
        UUIDType(binary=False),
        db.ForeignKey(SubCriteria.id),
    )
    is_compliant = db.Column(
        "is_compliant",
        db.Boolean(),
    )

    def __repr__(self):
        return f"""Compliance(
                sub_criteria_id={self.sub_criteria_id},
                assessment_id={self.assessment_id},
                is_compliant={self.is_compliant},
            )"""

    def __str__(self):
        return f"""< Subcriteria of {self.sub_criteria_id},
                for assessment {self.assessment_id},
                has compliant status set to {self.is_compliant}>"""

    def as_json(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "assessment_id": self.assessment_id,
            "sub_criteria_id": self.sub_criteria_id,
            "is_compliant": self.is_compliant,
        }


class ComplianceError(Exception):
    """Exception raised for errors in Sub-Criteria management
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class ComplianceMethods:
    @staticmethod
    def get_compliance(
        sub_criteria_id: str, assessment_id: str, return_as_json=False
    ):
        try:
            compliance = (
                db.session.query(Compliance)
                .filter(
                    Compliance.assessment_id == assessment_id,
                    Compliance.sub_criteria_id == sub_criteria_id,
                )
                .one()
            )
        except NoResultFound:
            raise IndexError
        if return_as_json:
            return [record.as_json() for record in compliance]
        return compliance

    @staticmethod
    def get_by_id(compliance_id: str):
        compliance = Compliance.query.get(compliance_id)
        if not compliance:
            raise Compliance(message="Compliance record could not be found")
        return compliance

    @staticmethod
    def register_compliance(
        sub_criteria_id: str,
        assessment_id: str,
        is_compliant: bool,
    ):
        try:
            is_compliant_record = Compliance(
                sub_criteria_id=sub_criteria_id,
                assessment_id=assessment_id,
                is_compliant=is_compliant,
            )
            db.session.add(is_compliant_record)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ComplianceError()
        return is_compliant_record