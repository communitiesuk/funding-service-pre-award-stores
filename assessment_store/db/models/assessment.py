import uuid

from db import db
from sqlalchemy.exc import IntegrityError


class Assessment(db.Model):
    id = db.Column(
        "id",
        db.Text(),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    status = db.Column(db.Text(length=36), default="UNASSESSED")
    application_id = db.Column(db.Text(), index=True, unique=True)

    def __repr__(self):
        return f"<Assessment {self.id} for Application {self.application_id}>"

    def as_json(self):
        return {
            "id": self.id,
            "status": self.status,
            "applicationId": self.application_id,
        }


class AssessmentError(Exception):
    """Exception raised for errors in Assessment management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class AssessmentMethods:
    @staticmethod
    def assessments(as_json=False):
        assessments = Assessment.query.all()
        if as_json:
            return [assessment.as_json() for assessment in assessments]
        return assessments

    @staticmethod
    def get_by_id(assessment_id: str):
        assessment = Assessment.query.get(assessment_id)
        if not assessment:
            raise AssessmentError(message="Assessment could not be found")
        return assessment

    @staticmethod
    def register_application(application_id: str):
        try:
            assessment = Assessment(application_id=application_id)
            db.session.add(assessment)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise AssessmentError(
                message="An assessment for this application already exists"
            )
        return assessment

    @staticmethod
    def update_status(assessment_id: str, status: str):
        try:
            assessment_id = AssessmentMethods.get_by_id(assessment_id)
            assessment_id.status = status
            db.session.commit()
            assessment = Assessment(
                application_id=assessment_id.application_id,
                id=assessment_id.id,
                status=assessment_id.status,
            )
            return assessment
        except AttributeError:
            raise AssessmentError(message="An assessment id doesn't not exist")
