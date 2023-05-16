from db import db
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


BaseModel: DefaultMeta = db.Model


class FormName(BaseModel):
    section_id = Column(
        "section_id",
        Integer,
        ForeignKey("section.id"),
        nullable=False,
        primary_key=True,
    )
    form_name = Column("form_name", db.String(), primary_key=True)
