from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from proto.common.data.models.fund import Fund, FundingType


class FundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fund

    funding_type = fields.Enum(FundingType)
