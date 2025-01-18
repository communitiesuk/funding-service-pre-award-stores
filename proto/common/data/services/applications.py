import random
import string

from sqlalchemy import delete, select

from db import db
from proto.common.data.models import ProtoApplication


def _generate_application_code():
    return "".join(random.choices(string.ascii_uppercase, k=6))


def create_application(preview: bool, round_id: int, account_id: str):
    if preview:
        db.session.execute(
            delete(ProtoApplication).filter(
                ProtoApplication.fake.is_(True),
                ProtoApplication.round_id == round_id,
                ProtoApplication.account_id == account_id,
            )
        )

    application = ProtoApplication(
        code=_generate_application_code(), fake=preview, round_id=round_id, account_id=account_id
    )
    db.session.add(application)
    db.session.commit()
    return application


def get_application(application_id: int):
    return db.session.scalars(select(ProtoApplication).filter(ProtoApplication.id == application_id)).one()
