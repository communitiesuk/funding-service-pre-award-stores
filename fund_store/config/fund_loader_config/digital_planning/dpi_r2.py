from datetime import datetime
from datetime import timezone

from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    DPI_R2_BASE_PATH,
)
from config.fund_loader_config.logo import DLUHC_LOGO_PNG

DPI_FUND_ID = "f493d512-5eb4-11ee-8c99-0242ac120002"
DPI_ROUND_2_ID = "0059aad4-5eb5-11ee-8c99-0242ac120002"
APPLICATION_BASE_PATH = ".".join([str(DPI_R2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(DPI_R2_BASE_PATH), str(2)])
DPI_R2_OPENS_DATE = datetime(
    2023, 10, 17, 10, 0, 0, tzinfo=timezone.utc
)  # 2023-10-17 10:00:00
DPI_R2_DEADLINE_DATE = datetime(
    2023, 12, 1, 11, 59, 0, tzinfo=timezone.utc
)  # 2023-11-1 11:59:00
DPI_R2_ASSESSMENT_DEADLINE_DATE = datetime(
    2024, 1, 31, 12, 0, 0, tzinfo=timezone.utc
)  # 2023-01-31 12:00:00

DPI_PROSPECTS_LINK = ""  # noqa
DPI_PRIVACY_NOTICE = ""  # TODO(adamdavies1) to be added
DPI_APPLICATION_GUIDANCE = (
    "<h2 class='govuk-heading govuk-heading-s'>Before you start</h2><p"
    f" class='govuk-body'><a href='{DPI_PROSPECTS_LINK}'>Read the fund's prospectus</a>"
    " before you apply.</p><p class='govuk-body'>You can <a"
    " href='{all_questions_url}'>preview the full list of application"
    " questions</a>.</p>"
)

r2_application_sections = [
    {
        "section_name": {"en": "Before you start", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {"en": "Name your application", "cy": ""},
        "form_name_json": {"en": "name-your-application", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": {"en": "1. About your organisation", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "1.1 Organisation information", "cy": ""},
        "form_name_json": {"en": "organisation-information-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": {"en": "2. Your skills and experience", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 50,
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "2.1 Your skills and experience", "cy": ""},
        "form_name_json": {"en": "your-skills-and-experience-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": {"en": "2.2 Roles and recruitment", "cy": ""},
        "form_name_json": {"en": "roles-and-recruitment-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
    },
    {
        "section_name": {"en": "3. About your project", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 50,
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "3.1 Engaging the ODP community", "cy": ""},
        "form_name_json": {"en": "engaging-the-odp-community-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": {"en": "3.2 Engaging the organisation", "cy": ""},
        "form_name_json": {"en": "engaging-the-organisation-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
    },
    {
        "section_name": {"en": "3.3 Dataset information", "cy": ""},
        "form_name_json": {"en": "dataset-information-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
    },
    {
        "section_name": {"en": "4. Future work", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "4.1 Future work", "cy": ""},
        "form_name_json": {"en": "future-work-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": {"en": "5. Declarations", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
    },
    {
        "section_name": {"en": "5.1 Declarations", "cy": ""},
        "form_name_json": {"en": "declarations-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
]

fund_config = {
    "id": DPI_FUND_ID,
    "name_json": {
        "en": "Digital Planning Improvement Fund",
        "cy": "",
    },
    "title_json": {
        "en": "funding to begin your digital planning improvement journey",
        "cy": "",
    },
    "short_name": "DPI",
    "description_json": {"en": "", "cy": ""},
    "welsh_available": False,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

round_config = [
    {
        "id": DPI_ROUND_2_ID,
        "fund_id": DPI_FUND_ID,
        "title_json": {"en": "Round 2", "cy": ""},
        "short_name": "R2",
        "opens": DPI_R2_OPENS_DATE,
        "deadline": DPI_R2_DEADLINE_DATE,
        "assessment_deadline": DPI_R2_ASSESSMENT_DEADLINE_DATE,
        "prospectus": DPI_PROSPECTS_LINK,
        "privacy_notice": DPI_PRIVACY_NOTICE,
        "contact_email": "digitalplanningteam@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions": "",
        "feedback_link": "",
        "project_name_field_id": "JAAhRP",
        "application_guidance": DPI_APPLICATION_GUIDANCE,
        "guidance_url": "",
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": False,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": True,
        "feedback_survey_config": {
            "requires_survey": True,
            "isSurveyOptional": True,
        },
    }
]
