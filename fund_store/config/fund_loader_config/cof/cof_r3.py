from datetime import datetime
from datetime import timezone

from config.fund_loader_config.cof.shared import COF_APPLICATION_GUIDANCE
from config.fund_loader_config.cof.shared import fund_config
from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_R3W1_BASE_PATH,
)

COF_FUND_ID = fund_config["id"]
COF_ROUND_3_WINDOW_1_ID = "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762"
APPLICATION_BASE_PATH = ".".join([str(COF_R3W1_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(COF_R3W1_BASE_PATH), str(2)])
COF_R3_OPENS_DATE = datetime(
    2023, 5, 31, 11, 0, 0, tzinfo=timezone.utc
)  # 2023-05-31 11:00:00
COF_R3_DEADLINE_DATE = datetime(
    2023, 7, 12, 11, 59, 0, tzinfo=timezone.utc
)  # 2023-07-12 11:59:00
COF_R3_ASSESSMENT_DEADLINE_DATE = datetime(
    2023, 8, 9, 12, 0, 0, tzinfo=timezone.utc
)  # 2023-08-09 12:00:00

cof_r3w1_sections = [
    {
        "section_name": {
            "en": "1. About your organisation",
            "cy": "1. Ynglŷn â'ch sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {
            "en": "1.1 Organisation information",
            "cy": "1.1 Gwybodaeth am y sefydliad",
        },
        "form_name_json": {
            "en": "organisation-information-cof-r3-w1",
            "cy": "gwybodaeth-am-y-sefydliad-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": {
            "en": "1.2 Applicant information",
            "cy": "1.2 Gwybodaeth am yr ymgeisydd",
        },
        "form_name_json": {
            "en": "applicant-information-cof-r3-w1",
            "cy": "gwybodaeth-am-yr-ymgeisydd-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.1.2",
    },
    {
        "section_name": {
            "en": "2. About your project",
            "cy": "2. Ynglŷn â'ch prosiect",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
    },
    {
        "section_name": {
            "en": "2.1 Project information",
            "cy": "2.1 Gwybodaeth am y prosiect",
        },
        "form_name_json": {
            "en": "project-information-cof-r3-w1",
            "cy": "gwybodaeth-am-y-prosiect-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": {
            "en": "2.2 Asset information",
            "cy": "2.2 Gwybodaeth am yr ased",
        },
        "form_name_json": {
            "en": "asset-information-cof-r3-w1",
            "cy": "gwybodaeth-am-yr-ased-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
    },
    {
        "section_name": {"en": "3. Strategic case", "cy": "3. Achos strategol"},
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 53,
    },
    {
        "section_name": {"en": "3.1 Community use", "cy": "3.1 Defnydd cymunedol"},
        "form_name_json": {
            "en": "community-use-cof-r3-w1",
            "cy": "defnydd-cymunedol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": {
            "en": "3.2 Community engagement",
            "cy": "3.2 Ymgysylltu â'r gymuned",
        },
        "form_name_json": {
            "en": "community-engagement-cof-r3-w1",
            "cy": "ymgysylltiad-cymunedol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
    },
    {
        "section_name": {"en": "3.3 Local support", "cy": "3.3 Cefnogaeth leol"},
        "form_name_json": {
            "en": "local-support-cof-r3-w1",
            "cy": "cefnogaeth-leol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.3.3",
    },
    {
        "section_name": {
            "en": "3.4 Community benefits",
            "cy": "3.4 Buddion i'r gymuned",
        },
        "form_name_json": {
            "en": "community-benefits-cof-r3-w1",
            "cy": "buddion-cymunedol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.3.4",
    },
    {
        "section_name": {
            "en": "3.5 Environmental sustainability",
            "cy": "3.5 Cynaliadwyedd amgylcheddol",
        },
        "form_name_json": {
            "en": "environmental-sustainability-cof-r3-w1",
            "cy": "cynaliadwyedd-amgylcheddol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.3.5",
    },
    {
        "section_name": {"en": "4. Management case", "cy": "4. Achos rheoli"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 47,
    },
    {
        "section_name": {
            "en": "4.1 Funding required",
            "cy": "4.1 Cyllid sydd ei angen",
        },
        "form_name_json": {
            "en": "funding-required-cof-r3-w1",
            "cy": "cyllid-sydd-ei-angen-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": {"en": "4.2 Feasibility", "cy": "4.2 Dichonoldeb"},
        "form_name_json": {
            "en": "feasibility-cof-r3-w1",
            "cy": "dichonoldeb-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
    },
    {
        "section_name": {"en": "4.3 Risk", "cy": "4.3 Risg"},
        "form_name_json": {"en": "risk-cof-r3-w1", "cy": "risg-cof-r3-w1"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
    },
    {
        "section_name": {"en": "4.4 Operational costs", "cy": "4.4 Costau gweithredol"},
        "form_name_json": {
            "en": "operational-costs-cof-r3-w1",
            "cy": "costau-gweithredol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.4",
    },
    {
        "section_name": {
            "en": "4.5 Skills and resources",
            "cy": "4.5 Sgiliau ac Adnoddau",
        },
        "form_name_json": {
            "en": "skills-and-resources-cof-r3-w1",
            "cy": "sgiliau-ac-adnoddau-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.5",
    },
    {
        "section_name": {
            "en": "4.6 Community representation",
            "cy": "4.6 Cynrychiolaeth gymunedol",
        },
        "form_name_json": {
            "en": "community-representation-cof-r3-w1",
            "cy": "cynrychiolaeth-gymunedol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.6",
    },
    {
        "section_name": {
            "en": "4.7 Inclusiveness and integration",
            "cy": "4.7 Cynhwysiant ac Integreiddio",
        },
        "form_name_json": {
            "en": "inclusiveness-and-integration-cof-r3-w1",
            "cy": "cynhwysiant-ac-integreiddio-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.7",
    },
    {
        "section_name": {
            "en": "4.8 Upload business plan",
            "cy": "4.8 Lanlwythwch y cynllun busnes",
        },
        "form_name_json": {
            "en": "upload-business-plan-cof-r3-w1",
            "cy": "lanlwythwch-y-cynllun-busnes-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.8",
    },
    {
        "section_name": {
            "en": "5. Subsidy control and state aid",
            "cy": "5. Rheoli cymorthdaliadau a chymorth gwladwriaethol",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
    },
    {
        "section_name": {
            "en": "5.1 Project qualification",
            "cy": "5.1 Cymhwystra'r prosiect",
        },
        "form_name_json": {
            "en": "project-qualifications-cof-r3-w1",
            "cy": "cymhwysedd-y-prosiect-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": {"en": "6. Check declarations", "cy": "6. Gwirio datganiadau"},
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
    },
    {
        "section_name": {"en": "6.1 Declarations", "cy": "6.1 Datganiadau"},
        "form_name_json": {
            "en": "declarations-cof-r3-w1",
            "cy": "cadarnhadau-terfynol-cof-r3-w1",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
]

round_config = [
    {
        "id": COF_ROUND_3_WINDOW_1_ID,
        "fund_id": COF_FUND_ID,
        "title_json": {"en": "Round 3 Window 1", "cy": "Round 3 Window 1"},
        "short_name": "R3W1",
        "opens": COF_R3_OPENS_DATE,
        "deadline": COF_R3_DEADLINE_DATE,
        "assessment_deadline": COF_R3_ASSESSMENT_DEADLINE_DATE,
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
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "apGjFS",
        "application_guidance": COF_APPLICATION_GUIDANCE,
    }
]
