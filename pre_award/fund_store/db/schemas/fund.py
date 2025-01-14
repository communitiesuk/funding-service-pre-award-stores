from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from pre_award.fund_store.db.models.fund import Fund, FundingType


class FundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fund

    funding_type = fields.Enum(FundingType)