from datetime import datetime
from datetime import timezone

from config.fund_loader_config.cof.eoi_r1_schema import COF_R3_EOI_SCHEMA
from config.fund_loader_config.cof.shared import EOI_APPLICATION_GUIDANCE
from config.fund_loader_config.cof.shared import fund_config
from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_EOI_BASE_PATH,
)
from config.fund_loader_config.logo import DLUHC_LOGO_PNG

COF_FUND_ID = "54c11ec2-0b16-46bb-80d2-f210e47a8791"
COF_EOI_ROUND_ID = "6a47c649-7bac-4583-baed-9c4e7a35c8b3"

APPLICATION_BASE_PATH_COF_EOI = ".".join([str(COF_EOI_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH_COF_EOI = ".".join([str(COF_EOI_BASE_PATH), str(2)])

COF_EOI_OPENS_DATE = datetime(2024, 3, 6, 11, 00, 0, tzinfo=timezone.utc)  # 2023-12-06 11:00:00
COF_EOI_DEADLINE_DATE = datetime(2124, 3, 6, 11, 59, 0, tzinfo=timezone.utc)  # 2124-03-06 11:59:00
COF_EOI_ASSESSMENT_DEADLINE_DATE = datetime(2124, 3, 6, 12, 0, 0, tzinfo=timezone.utc)  # 2124-03-06 12:00:00
COF_EOI_SEND_REMINDER_DATE = datetime(2024, 3, 1, 11, 59, 0, tzinfo=timezone.utc)  # 2024-03-1 11:59:00


fund_config = {
    "id": COF_FUND_ID,
    "name_json": {
        "en": "Community Ownership Fund",
        "cy": "Y Cronfa Perchnogaeth Gymunedol",
    },
    "title_json": {
        "en": "expression of interest in applying for Community Ownership Fund",
        "cy": "",
    },
    "short_name": "COF-EOI",
    "description_json": fund_config["description_json"],
    "welsh_available": True,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

cof_eoi_sections = [
    {
        "section_name": {
            "en": "1. Expression of interest",
            "cy": "",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "1.1 Organisation details",
            "cy": "",
        },
        "form_name_json": {
            "en": "cof-eoi-details",
            "cy": "",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.1",
    },
    {
        "section_name": {
            "en": "1.2 About your asset",
            "cy": "",
        },
        "form_name_json": {
            "en": "cof-eoi-asset",
            "cy": "",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.2",
    },
    {
        "section_name": {
            "en": "1.3 Your funding request",
            "cy": "",
        },
        "form_name_json": {
            "en": "cof-eoi-funding",
            "cy": "",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.3",
    },
    {
        "section_name": {
            "en": "1.4 Development support provider",
            "cy": "",
        },
        "form_name_json": {
            "en": "cof-eoi-support",
            "cy": "",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.4",
    },
    {
        "section_name": {
            "en": "1.5 Declaration",
            "cy": "",
        },
        "form_name_json": {
            "en": "cof-eoi-declatation",
            "cy": "",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_EOI}.1.5",
    },
]

round_config_eoi = [
    {
        "id": COF_EOI_ROUND_ID,
        "fund_id": COF_FUND_ID,
        "title_json": {"en": "Expression of interest", "cy": ""},
        "short_name": "R1",
        "opens": COF_EOI_OPENS_DATE,
        "assessment_start": None,
        "deadline": COF_EOI_DEADLINE_DATE,
        "application_reminder_sent": False,
        "reminder_date": COF_EOI_SEND_REMINDER_DATE,
        "assessment_deadline": COF_EOI_ASSESSMENT_DEADLINE_DATE,
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
            "You must complete this Expression of Interest (EOI) form if you"
            " areinterested in applying for the Community Ownership Fund (COF). <a"
            ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus"'
            " Read the fund's prospectus before you start.</a>."
        ),
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "",
        "application_guidance": EOI_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://www.gov.uk/government/publications/community-ownership-fund-round-3-application-form"
            "-assessment-criteria-guidance"
        ),
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": True,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": False,
        "feedback_survey_config": {
            "has_feedback_survey": False,
            "has_section_feedback": True,
            "is_feedback_survey_optional": False,
            "is_section_feedback_optional": False,
        },
        "eligibility_config": {"has_eligibility": False},
        "eoi_decision_schema": COF_R3_EOI_SCHEMA,
    }
]
