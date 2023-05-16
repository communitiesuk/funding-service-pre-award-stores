from db.models.fund import Fund
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class FundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fund
