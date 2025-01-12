from datetime import date

import psycopg2
import sqlalchemy.exc
from flask_babel import gettext as _
from sqlalchemy import select

from db import db
from proto.common.data.exceptions import DataValidationError
from proto.common.data.models.fund import Fund, ProtoGrantSchema
from proto.common.data.models.round import Round


def get_grant(short_code: str):
    grant = db.session.scalars(select(Fund).filter(Fund.short_name == short_code)).one()
    return grant


def get_active_round(grant_short_code: str):
    round = db.session.scalars(
        select(Round)
        .join(Fund)
        .filter(
            Fund.short_name == grant_short_code,
            # probably want some way of having rounds that are always open especially for uncompeted grants
            Round.proto_start_date <= date.today(),
            Round.proto_end_date >= date.today(),
        )
    ).one_or_none()
    return round, round.proto_grant if round else None


def get_all_grants():
    return db.session.scalars(select(Fund)).all()


def create_grant(grant_data: ProtoGrantSchema):
    grant = Fund(
        name_json={"en": grant_data.name, "cy": grant_data.name_cy},  # Workaround: required field
        title_json={"en": grant_data.name, "cy": grant_data.name_cy},  # Workaround: required field
        short_name=grant_data.short_code,
        description_json={"en": grant_data.name, "cy": grant_data.name_cy},  # Workaround: required field
        owner_organisation_name="todo",  # Workaround: required field
        owner_organisation_shortname="todo",  # Workaround: required field
        owner_organisation_logo_uri="todo",  # Workaround: required field
        funding_type=grant_data.funding_type,
        ggis_scheme_reference_number=grant_data.ggis_scheme_reference_number,
        proto_name=grant_data.name,
        proto_name_cy=grant_data.name_cy,
        proto_prospectus_link=grant_data.prospectus_link,
    )
    db.session.add(grant)

    try:
        db.session.commit()  # TODO: plan for transaction management

    except sqlalchemy.exc.IntegrityError as e:
        cause = e.__cause__
        if isinstance(cause, psycopg2.errors.UniqueViolation) and "Key (short_name)=" in cause.diag.message_detail:
            raise DataValidationError(
                message=_(f"A grant with the code ‘{grant_data.short_code}’ already exists. Enter a different code."),
                schema_field_name="short_code",
            ) from e
