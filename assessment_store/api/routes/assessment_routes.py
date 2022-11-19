# flake8: noqa
from db.queries.assessment_records import get_metadata_for_fund_round_id


def all_assessments_for_fund_round_id(fund_id, round_id):

    app_list = get_metadata_for_fund_round_id(
        fund_id=fund_id, round_id=round_id
    )

    return app_list
