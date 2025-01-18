from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from proto.common.data.models.types import pk_int

if TYPE_CHECKING:
    from account_store.db.models import Account
    from proto.common.data.models import Round


class ProtoApplication(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    code: Mapped[str]
    fake: Mapped[bool]  # hack: true if this is a 'previewed' application (grant admin feature)

    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"))
    round: Mapped["Round"] = relationship("Round")
    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship("Account")


class ProtoApplicationSectionData(db.Model):
    id: Mapped[pk_int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

    data: Mapped[dict] = mapped_column(nullable=False, default=dict)

    proto_application_id: Mapped[int] = mapped_column(ForeignKey("proto_application.id"))
    proto_application: Mapped["Round"] = relationship("ProtoApplication")
