from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from db.models.event import Event, EventType


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event

    round_id = auto_field()
    type = fields.Enum(EventType)
