#!/usr/bin/env python3
# flake8: noqa
from app import app  # noqa: E402
from config import Config  # noqa: E402
from db.queries import insert_application_sections
from db.queries import insert_assessment_sections
from db.queries import insert_fund_data
from db.queries import insert_round_data
from db.queries import upsert_fields
from scripts.deprecated_fund_config import cof_form_config
from scripts.deprecated_fund_config.assessment_section_config import scored_sections
from scripts.deprecated_fund_config.assessment_section_config import (
    unscored_sections,
)
from scripts.deprecated_fund_config.sort_application_sections import (
    return_numerically_sorted_section_for_application,
)
from scripts.deprecated_fund_config.sort_assessment_sections import (
    return_numerically_sorted_section_for_assessment,
)


def create_sections(path_prefix, round_id, forms_config):
    tree_base_sections = [
        {
            "section_name": "Application",
            "tree_path": f"{path_prefix}.1",
            "weighting": None,
        },
        {
            "section_name": "Assessment",
            "tree_path": f"{path_prefix}.2",
            "weighting": None,
        },
    ]

    # assessment_config = return_numerically_sorted_section_for_assessment(scored_sections, unscored_sections)
    print(f"Inserting base sections config.")
    insert_application_sections(round_id, tree_base_sections)
    # -- load fields belonging to round --
    # inserted_field_ids = upsert_fields(assessment_config["all_fields"])

    # -- load application sections --
    if forms_config:
        # -- convert old config into new config (stage not necessary for new rounds) --
        sorted_application_sections = return_numerically_sorted_section_for_application(
            forms_config, tree_base_sections[0]["tree_path"]
        )["sorted_sections"]
        print(f"Inserting forms config.")
        insert_application_sections(round_id, sorted_application_sections)
    # assessment_result = insert_assessment_sections(cof_form_config.COF_ROUND_2_ID, assessment_config)

if __name__ == "__main__":
    with app.app_context():

        # -- load fund and rounds --
        fund_config = {
            "id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
            "name": "Community Ownership Fund",
            "title": "funding to save an asset in your community",
            "short_name": "COF",
            "description": (
                "The Community Ownership Fund is a £150 million fund over 4 years"
                " to support community groups across England, Wales, Scotland and"
                " Northern Ireland to take ownership of assets which are at risk"
                " of being lost to the community."
            ),
        }

        rounds_config = [
            {
                "id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
                "title": "Round 2 Window 2",
                "short_name": "R2W2",
                "opens": "2022-10-04 12:00:00",
                "deadline": "2022-12-14 11:59:00",
                "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
                "assessment_deadline": "2023-03-30 12:00:00",
                "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
                "privacy_notice": "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/community-ownership-fund-privacy-notice",
                "contact_email": "COF@levellingup.gov.uk",
                "contact_phone": None,
                "contact_textphone": None,
                "support_times": "9am to 5pm",
                "support_days": "Monday to Friday",
                "instructions": (
                    "You must have received an invitation to apply. If we did not invite"
                    " you, first <a"
                    ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
                    " express your interest in the fund</a>."
                ),
            },
            {
                "id": "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
                "title": "Round 2 Window 3",
                "short_name": "R2W3",
                "opens": "2022-10-04 12:00:00",
                "deadline": "2022-12-14 11:59:00",
                "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
                "assessment_deadline": "2023-03-30 12:00:00",
                "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
                "privacy_notice": "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/community-ownership-fund-privacy-notice",
                "contact_email": "COF@levellingup.gov.uk",
                "contact_phone": None,
                "contact_textphone": None,
                "support_times": "9am to 5pm",
                "support_days": "Monday to Friday",
                "instructions": (
                    "You must have received an invitation to apply. If we did not invite"
                    " you, first <a"
                    ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
                    " express your interest in the fund</a>."
                ),
            },
        ]

        inserted_fund = insert_fund_data(fund_config)
        print("Fund inserted:")
        print(inserted_fund)
        inserted_rounds = insert_round_data(rounds_config)
        print("Rounds inserted:")
        print(inserted_rounds)

        # Do we want to reuse the application sections config?

        # Separate config for r2w2 and r2w3
        # create_sections("1", cof_form_config.COF_ROUND_2_ID, cof_form_config.COF_R2_ORDERED_FORMS_CONFIG, True)
        # create_sections("2", cof_form_config.COF_ROUND_2_W3_ID, cof_form_config.COF_R2_ORDERED_FORMS_CONFIG, True)

        # reuse config between r2w2 and r2w3
        create_sections(
            "1",
            cof_form_config.COF_ROUND_2_ID,
            cof_form_config.COF_R2_ORDERED_FORMS_CONFIG,
        )
        create_sections("1", cof_form_config.COF_ROUND_2_W3_ID, None)
