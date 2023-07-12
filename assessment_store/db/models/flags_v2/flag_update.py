from enum import IntEnum
from uuid import uuid4

from db import db
from flask_sqlalchemy import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

BaseModel: DefaultMeta = db.Model


class FlagStatus(IntEnum):
    # QA_COMPLETE used to be assigned value 2, but this has been removed from being a flag
    # and is now a seperate workflow. Inorder to not lose existing QA complete data, we have
    # not reassigned RESOLVED to value 2 (which would cascaded delete QA_COMPLETE values in
    # the flag column) but kept it as 3. 
    RAISED = 0
    STOPPED = 1
    RESOLVED = 3


class FlagUpdate(BaseModel):

    __tablename__ = "flag_update"

    id = Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True)
    assessment_flag_id = Column(
        "assessment_flag_id",
        UUID(as_uuid=True),
        ForeignKey("assessment_flag.id"),
    )
    user_id = Column("user_id", String, nullable=False)
    date_created = Column(
        "date_created", db.DateTime(), server_default=func.now()
    )
    justification = Column("justification", String)
    status = Column("status", ENUM(FlagStatus))
    allocation = Column("allocation", String)
