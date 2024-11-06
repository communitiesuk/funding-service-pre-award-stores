from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field

from db.models.round import Round


class RoundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Round
        exclude = ["eoi_decision_schema"]

    fund_id = auto_field()
