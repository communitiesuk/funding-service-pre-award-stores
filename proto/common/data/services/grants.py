from sqlalchemy import select

from db import db
from proto.common.data.models.fund import Fund


# PROTO: decision - only look up by external ID, if you don't have it don't look it up?
# if we want short codes in the URL then potentially that could be a reason for an override
def get_grant(external_id: str):
    grants = db.session.scalars(select(Fund)).all()
    return grants
