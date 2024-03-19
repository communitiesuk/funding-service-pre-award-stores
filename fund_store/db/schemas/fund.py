from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db.models.fund import Fund


class FundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fund
