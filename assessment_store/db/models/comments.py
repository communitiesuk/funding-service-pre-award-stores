import uuid
from db import db
from datetime import datetime
from xml.etree.ElementTree import Comment
from db.models.assessment import Assessment
from db.models.sub_criteria import SubCriteria
from sqlalchemy import DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils.types import UUIDType
from sqlalchemy.exc import StatementError

class Comment(db.Model):
    id = db.Column(
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    comment = db.Column(
        db.Text(),
    )
    created_at = db.Column(
        DateTime(), 
        default=datetime.utcnow
    )
    assessment_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey(Assessment.id),
    )
    assessor_user_id = db.Column(
        db.Text(),
    )
    sub_criteria_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey(SubCriteria.id),
        nullable=False,
    )
    section_id = db.Column(
        db.Integer(),
        nullable=False
    )

    def __repr__(self):
        return f"""Comments(
                sub_criteria_id={self.sub_criteria_id},
                assessment_id={self.assessment_id},
                comment={self.comment},
                assessor_user_id={self.assessor_user_id},
            )"""

    def __str__(self):
        return f"<comment of {self.comment} \
                for Sub-Criteria {str(self.sub_criteria_id)} \
                of Assessment {str(self.assessment_id)} \
                by Person {self.assessor_user_id}>"

    def as_json(self):
        return {
            "id": str(self.id),
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "assessment_id": str(self.assessment_id),
            "assessor_user_id": self.assessor_user_id,
            "sub_criteria_id": str(self.sub_criteria_id),
            "comment": self.comment,
        }


class CommentError(Exception):
    """Exception raised for errors in Sub-Criteria management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="There was a problem with the database query."):
        self.message = message
        super().__init__(self.message)


class CommentMethods:

    @staticmethod
    def get_by_comment_id(id: str):
        comment = Comment.query.get(id)
        if not comment:
            raise CommentError(
                message="Comment could not be found"
            )
        return comment

    @staticmethod
    def get_section_comments(
        assessment_id: str, sub_criteria_id: str, section_id: int, as_json=False
    ):
        try:
            comments = (
                db.session.query(Comment)
                .filter(
                    Comment.assessment_id == assessment_id,
                    Comment.sub_criteria_id == sub_criteria_id,
                    Comment.section_id == section_id,
                )
                .all()
            )
            if as_json:
                return [record.as_json() for record in comments]
        except StatementError as e:
            db.session.rollback()
            message = e.orig.args[0] if e.orig else f"There was a StatementError following the database query: {e.statment}"
            raise CommentError(message)
        return comments

    @staticmethod
    def save_comment(
        assessment_id: str,
        sub_criteria_id: str,
        section_id: int,
        assessor_user_id: str,
        comment: str,
    ):
        try:
            comment = Comment(
                assessment_id=assessment_id,
                sub_criteria_id=sub_criteria_id,
                section_id=section_id,
                comment=comment,
                assessor_user_id=assessor_user_id,
            )
            db.session.add(comment)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            message = e.orig.pgerror if e.orig else f"There was a IntegrityError following the database query: {e.statment}"
            raise CommentError(message)
        except StatementError as e:
            db.session.rollback()
            message = e.orig.args[0] if e.orig else f"There was a StatementError following the database query: {e.statment}"
            raise CommentError(message)
        return comment
