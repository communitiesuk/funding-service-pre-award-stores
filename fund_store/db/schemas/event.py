from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field

from db.models.event import Event
from db.models.event import EventType


class EventSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Event

    round_id = auto_field()
    type = fields.Enum(EventType)
