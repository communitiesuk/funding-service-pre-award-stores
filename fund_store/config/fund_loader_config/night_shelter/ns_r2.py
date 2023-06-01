from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    NSTF_R2_BASE_PATH,
)

NIGHT_SHELTER_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NIGHT_SHELTER_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"
APPLICATION_BASE_PATH = ".".join([str(NSTF_R2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(NSTF_R2_BASE_PATH), str(2)])

r2_application_sections = [
    {
        "section_name": "Before you start",
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": "Name you application",
        "form_name": "name-your-application-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": "1. About your organisation",
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
    },
    {
        "section_name": "1.1 Organisation Information",
        "form_name": "organisation-information-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": "1.2 Organisation type",
        "form_name": "organisation-type-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
    },
    {
        "section_name": "1.3 Applicant information",
        "form_name": "applicant-information-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.3",
    },
    {
        "section_name": "1.4 Joint applications",
        "form_name": "joint-applications-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.4",
    },
    {
        "section_name": "2. Your skills and experience",
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 10,
    },
    {
        "section_name": "2.1 Staff and volunteers",
        "form_name": "staff-and-volunteers-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": "2.2 Current services",
        "form_name": "current-services-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
    },
    {
        "section_name": "3. Your proposal",
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 45,
    },
    {
        "section_name": "3.1 Objectives and activities",
        "form_name": "objectives-and-activities-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": "3.2 Project milestones",
        "form_name": "project-milestones-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
    },
    {
        "section_name": "3.3 Local need and support",
        "form_name": "local-need-and-support-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
    },
    {
        "section_name": "3.4 Proposed services",
        "form_name": "proposed-services-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.4",
    },
    {
        "section_name": "3.5 Working in partnership",
        "form_name": "working-in-partnership-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.5",
    },
    {
        "section_name": "3.6 Proposal sustainability",
        "form_name": "proposal-sustainability-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.6",
    },
    {
        "section_name": "4. Outputs and outcomes",
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "weighting": 15,
    },
    {
        "section_name": "4.1 Outputs and outcomes",
        "form_name": "outputs-and-outcomes-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": "5. Risk and deliverability",
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
        "weighting": 15,
    },
    {
        "section_name": "5.1 Risk and deliverability",
        "form_name": "risk-and-deliverability-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
    {
        "section_name": "6. Value for money",
        "tree_path": f"{APPLICATION_BASE_PATH}.7",
        "weighting": 15,
    },
    {
        "section_name": "6.1 Funding required",
        "form_name": "funding-required-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.7.1",
    },
    {
        "section_name": "6.2 Building works",
        "form_name": "building-works-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.7.2",
    },
    {
        "section_name": "6.3 Match funding",
        "form_name": "match-funding-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.7.3",
    },
    {
        "section_name": "7. Check declarations",
        "tree_path": f"{APPLICATION_BASE_PATH}.8",
    },
    {
        "section_name": "7.1 Declarations",
        "form_name": "declarations-ns",
        "tree_path": f"{APPLICATION_BASE_PATH}.8.1",
    },
]

fund_config = {
    "id": NIGHT_SHELTER_FUND_ID,
    "name": "Night Shelter Transformation Fund",
    "title": "funding to transform your night shelter services in England",
    "short_name": "NSTF",
    "description": "",
    "welsh_available": False,
}

round_config = [
    {
        "id": NIGHT_SHELTER_ROUND_2_ID,
        "fund_id": NIGHT_SHELTER_FUND_ID,
        "title": "Round 2",
        "short_name": "R2",
        "opens": "2023-06-07 12:00:00",
        "deadline": "2023-07-05 11:59:00",
        "assessment_deadline": "2023-08-09 12:00:00",
        "prospectus": "",
        "privacy_notice": "",
        "contact_email": "transformationfund@levellingup.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions": "",
        "feedback_link": "https://forms.office.com/e/n6J9KPebUy",
        "project_name_field_id": "YVsPtE",
        "application_guidance": None,
    }
]
