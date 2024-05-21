from marshmallow.fields import String
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field

from db.models.event import Event


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event

    round_id = auto_field()
    processed = String()
