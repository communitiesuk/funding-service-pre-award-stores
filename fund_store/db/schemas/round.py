from db.models.round import Round
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class RoundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Round

    fund_id = auto_field()
