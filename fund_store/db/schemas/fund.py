from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db.models.fund import Fund
from db.models.fund import FundingType


class FundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fund

    funding_type = fields.Enum(FundingType)
