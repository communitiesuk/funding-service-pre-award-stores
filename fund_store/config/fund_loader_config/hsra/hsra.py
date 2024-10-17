from datetime import datetime
from datetime import timezone

from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    HSRA_BASE_PATH,
)
from config.fund_loader_config.hsra.shared import HSRA_APPLICATION_GUIDANCE
from config.fund_loader_config.logo import DLUHC_LOGO_PNG
from db.models.fund import FundingType

HSRA_FUND_ID = "1e4bd8b0-b399-466d-bbd1-572171bbc7bd"
HSRA_ROUND_ID = "50062ff6-e696-474d-a560-4d9af784e6e5"

APPLICATION_BASE_PATH_HSRA = ".".join([str(HSRA_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH_HSRA = ".".join([str(HSRA_BASE_PATH), str(2)])

# TODO Dates are still being debated and are likely to change
HSRA_OPENS_DATE = datetime(2024, 6, 27, 11, 00, 0, tzinfo=timezone.utc)  # 2024-06-27 11:00:00
HSRA_START_DATE = datetime(2024, 6, 27, 11, 00, 0, tzinfo=timezone.utc)  # 2024-06-27 11:00:00
# TODO The bellow dates are likely to change when the fund is live
HSRA_SEND_REMINDER_DATE = datetime(2025, 1, 27, 11, 59, 0, tzinfo=timezone.utc)  # 2025-1-27 11:59:00
HSRA_DEADLINE_DATE = datetime(2025, 1, 29, 11, 00, 0, tzinfo=timezone.utc)  # 2025-01-29 11:00:00
HSRA_ASSESSMENT_DEADLINE_DATE = datetime(2024, 6, 23, 12, 0, 0, tzinfo=timezone.utc)  # 2024-06-23 12:00:00

hsra_sections = [
    {
        "section_name": {"en": "1. Application name", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.1",
    },
    {
        "section_name": {"en": "Name your application", "cy": ""},
        "form_name_json": {"en": "name-your-application-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.1.1",
    },
    {
        "section_name": {"en": "2. About your organisation", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.2",
    },
    {
        "section_name": {"en": "Organisation information", "cy": ""},
        "form_name_json": {"en": "organisation-information-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.2.1",
    },
    {
        "section_name": {"en": "Applicant information", "cy": ""},
        "form_name_json": {"en": "applicant-information-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.2.2",
    },
    {
        "section_name": {"en": "Joint applicant", "cy": ""},
        "form_name_json": {"en": "joint-applicant-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.2.3",
    },
    {
        "section_name": {"en": "3. About your project", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.3",
    },
    {
        "section_name": {"en": "Vacant property details", "cy": ""},
        "form_name_json": {"en": "vacant-property-details-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.3.1",
    },
    {
        "section_name": {"en": "Designated area details", "cy": ""},
        "form_name_json": {"en": "designated-area-details-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.3.2",
    },
    {
        "section_name": {"en": "Project milestones", "cy": ""},
        "form_name_json": {"en": "milestones-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.3.3",
    },
    {
        "section_name": {"en": "4. Project costs", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.4",
    },
    {
        "section_name": {"en": "Total expected cost", "cy": ""},
        "form_name_json": {"en": "total-expected-cost-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.4.1",
    },
    {
        "section_name": {"en": "Refurbishment costs", "cy": ""},
        "form_name_json": {"en": "refurbishment-costs-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.4.2",
    },
    {
        "section_name": {"en": "Other costs", "cy": ""},
        "form_name_json": {"en": "other-costs-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.4.3",
    },
    {
        "section_name": {"en": "5. Declaration", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.5",
    },
    {
        "section_name": {"en": "Declaration", "cy": ""},
        "form_name_json": {"en": "declaration-hsra", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH_HSRA}.5.1",
    },
]

fund_config = {
    "id": HSRA_FUND_ID,
    "name_json": {
        "en": "High Street Rental Auctions Fund",
        "cy": "",
    },
    "title_json": {
        "en": "funding to cover the cost of delivering a high street rental auction",
        "cy": "",
    },
    "short_name": "HSRA",
    "funding_type": FundingType.COMPETITIVE,
    "description_json": {"en": "", "cy": ""},
    "welsh_available": False,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

round_config = [
    {
        "id": HSRA_ROUND_ID,
        "fund_id": HSRA_FUND_ID,
        "title_json": {"en": "Round 1", "cy": "Rownd 1"},
        "short_name": "R1",
        "opens": HSRA_OPENS_DATE,
        "assessment_start": HSRA_START_DATE,
        "deadline": HSRA_DEADLINE_DATE,
        "application_reminder_sent": False,
        "reminder_date": HSRA_SEND_REMINDER_DATE,
        "assessment_deadline": HSRA_ASSESSMENT_DEADLINE_DATE,
        "prospectus": "",  # TODO needs to be added
        "privacy_notice": "",
        "reference_contact_page_over_email": False,
        "contact_us_banner_json": {"en": "", "cy": ""},
        "contact_email": "HighStreetRentalAuctions@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions_json": {
            "en": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="">'
                " express your interest in the fund</a>."
            ),  # TODO Need to guidance link
            "cy": (""),
        },
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "qbBtUh",
        "application_guidance_json": HSRA_APPLICATION_GUIDANCE,
        "guidance_url": "",  # TODO add guidance link
        "all_uploaded_documents_section_available": True,
        "application_fields_download_available": True,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": True,
        "is_expression_of_interest": False,
        "feedback_survey_config": {
            "has_feedback_survey": False,
            "has_section_feedback": False,
            "is_feedback_survey_optional": False,
            "is_section_feedback_optional": False,
        },
        "eligibility_config": {"has_eligibility": True},
        "eoi_decision_schema": None,
    }
]
