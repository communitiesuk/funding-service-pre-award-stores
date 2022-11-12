from db import db
from db.models.assessment_record import AssessmentRecords

from sqlalchemy import select
from sqlalchemy.orm import load_only

assessment_record_metadata = [
    AssessmentRecords.application_id,
    AssessmentRecords.fund_id,
    AssessmentRecords.round_id,
    AssessmentRecords.langauge,
    AssessmentRecords.project_name,
    AssessmentRecords.short_id,
    AssessmentRecords.type_of_application,
    AssessmentRecords.funding_amount_requested]

def get_metadata_for_fund_round_id(fund_id, round_id):

    stmt = select(AssessmentRecords).options(load_only(*assessment_record_metadata)).where(AssessmentRecords.fund_id == fund_id, AssessmentRecords.round_id == round_id)

    # scalars directly gets the row values rather than return RowProxy s. 
    assessment_metadatas = db.session.scalars(stmt).all()

    return assessment_metadatas