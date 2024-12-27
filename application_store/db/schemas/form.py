from marshmallow.fields import Enum
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from application_store.db.models import Forms
from application_store.db.models.forms.enums import Status


class FormsRunnerSchema(SQLAlchemySchema):
    class Meta:
        model = Forms

    status = Enum(Status)
    name = auto_field()
    questions = auto_field("json")
    has_completed = auto_field()
