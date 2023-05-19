#!/usr/bin/env python3
from db.queries import insert_application_sections
from db.queries import insert_fund_data
from db.queries import insert_round_data
from scripts.common_fund_config.fund_base_tree_paths import COF_R3W1_BASE_PATH

tree_base_sections = [
    {
        "section_name": "Application",
        "tree_path": f"{COF_R3W1_BASE_PATH}.1",
        "weighting": None,
    },
    {
        "section_name": "Assessment",
        "tree_path": f"{COF_R3W1_BASE_PATH}.2",
        "weighting": None,
    },
]


sorted_application_r3w1_sections = [
    {
        "section_name": "About your organisation",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.1",
    },
    {
        "section_name": "1.1 Organisation Information",
        "form_name": "organisation-information-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.1.1",
    },
    {
        "section_name": "1.2 Applicant Information",
        "form_name": "applicant-information-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.1.2",
    },
    {
        "section_name": "About your project",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.2",
    },
    {
        "section_name": "2.1 Project Information",
        "form_name": "project-information-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.2.1",
    },
    {
        "section_name": "2.2 Asset Information",
        "form_name": "asset-information-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.2.2",
    },
    {
        "section_name": "Strategic case",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.3",
    },
    {
        "section_name": "3.1 Community Use",
        "form_name": "community-use-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.3.1",
    },
    {
        "section_name": "3.2 Community Engagement",
        "form_name": "community-engagement-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.3.2",
    },
    {
        "section_name": "3.3 Local Support",
        "form_name": "local-support-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.3.3",
    },
    {
        "section_name": "3.4 Community benefits",
        "form_name": "community-benefits-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.3.4",
    },
    {
        "section_name": "3.5 Environmental Sustainability",
        "form_name": "environmental-sustainability-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.3.5",
    },
    {
        "section_name": "Management case",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4",
    },
    {
        "section_name": "4.1 Funding Required",
        "form_name": "funding-required-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.1",
    },
    {
        "section_name": "4.2 Feasibility",
        "form_name": "feasibility-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.2",
    },
    {
        "section_name": "4.3 Risk",
        "form_name": "risk-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.3",
    },
    {
        "section_name": "4.4 Operational costs",
        "form_name": "operational-costs-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.4",
    },
    {
        "section_name": "4.5 Skills and resources",
        "form_name": "skills-and-resources-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.5",
    },
    {
        "section_name": "4.6 Community representation",
        "form_name": "community-representation-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.6",
    },
    {
        "section_name": "4.7 Inclusiveness and integration",
        "form_name": "inclusiveness-and-integration-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.7",
    },
    {
        "section_name": "4.8 Upload business plan",
        "form_name": "upload-business-plan-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.4.8",
    },
    {
        "section_name": "Subsidy control and state aid",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.5",
    },
    {
        "section_name": "5.1 Project qualification",
        "form_name": "project-qualifications-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.5.1",
    },
    {
        "section_name": "Check declarations",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.6",
    },
    {
        "section_name": "6.1 Declarations",
        "form_name": "final-confirmations-cof-r3-w1",
        "tree_path": f"{tree_base_sections[0]['tree_path']}.6.1",
    },
]

COF_ROUND_3_WINDOW_1_ID = "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762"

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

round_config = [
    {
        "id": "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762",
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "title": "Round 3 Window 1",
        "short_name": "R3W1",
        "opens": "2023-05-31 12:00:00",
        "deadline": "2023-07-12 11:59:00",
        "assessment_deadline": "2023-08-09 12:00:00",
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-"
            "privacy-notice/community-ownership-fund-privacy-notice"
        ),
        "contact_email": "COF@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions": (
            "You must have received an invitation to apply. If we did not invite you,"
            " first <a"
            ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
            " express your interest in the fund</a>."
        ),
    }
]


def main() -> None:
    print("Inserting fund and round data.")
    insert_fund_data(fund_config)
    insert_round_data(round_config)

    print("Inserting base sections config.")
    insert_application_sections(COF_ROUND_3_WINDOW_1_ID, tree_base_sections)
    print("Inserting sections.")
    insert_application_sections(
        COF_ROUND_3_WINDOW_1_ID, sorted_application_r3w1_sections
    )


if __name__ == "__main__":
    from app import app

    with app.app_context():
        main()
