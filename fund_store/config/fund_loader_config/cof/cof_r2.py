from config.fund_loader_config.cof.shared import fund_config
from config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_R2_W2_BASE_PATH,
)

COF_FUND_ID = fund_config["id"]
COF_ROUND_2_WINDOW_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_WINDOW_3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
APPLICATION_BASE_PATH = ".".join([str(COF_R2_W2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(COF_R2_W2_BASE_PATH), str(2)])


rounds_config = [
    {
        "id": COF_ROUND_2_WINDOW_2_ID,
        "title": "Round 2 Window 2",
        "short_name": "R2W2",
        "opens": "2022-10-04 12:00:00",
        "deadline": "2022-12-14 11:59:00",
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "assessment_deadline": "2023-03-30 12:00:00",
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/"
            "community-ownership-fund-privacy-notice",
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
            "EGg0v32c3kOociSi7zmVqN48ORk8WN5LlJITE3Swt-lURUNCR0dHMjgxWFZOMTMxQzlOTVIxVkQ0Sy4u"
        ),
        "project_name_field_id": "KAgrBz",
    },
    {
        "id": COF_ROUND_2_WINDOW_3_ID,
        "title": "Round 2 Window 3",
        "short_name": "R2W3",
        "opens": "2022-10-04 12:00:00",
        "deadline": "2023-04-14 11:59:00",
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "assessment_deadline": "2023-05-17 12:00:00",
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/"
            "community-ownership-fund-privacy-notice"
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
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElUREIySU9OWTU4R0RTNjhBUDE1Q1VYVFBEMi4u"
        ),
        "project_name_field_id": "KAgrBz",
    },
]

cof_r2_sections = [
    {
        "section_name": "1. About your organisation",
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": "Organisation Information",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
        "form_name": "organisation-information",
    },
    {
        "section_name": "Applicant Information",
        "tree_path": f"{APPLICATION_BASE_PATH}.1.2",
        "form_name": "applicant-information",
    },
    {
        "section_name": "2. About your project",
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
    },
    {
        "section_name": "Project Information",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
        "form_name": "project-information",
    },
    {
        "section_name": "Asset Information",
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
        "form_name": "asset-information",
    },
    {
        "section_name": "3. Strategic case",
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 30,
    },
    {
        "section_name": "Community Use",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
        "form_name": "community-use",
    },
    {
        "section_name": "Community Engagement",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
        "form_name": "community-engagement",
    },
    {
        "section_name": "Local Support",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.3",
        "form_name": "local-support",
    },
    {
        "section_name": "Environmental Sustainability",
        "tree_path": f"{APPLICATION_BASE_PATH}.3.4",
        "form_name": "environmental-sustainability",
    },
    {
        "section_name": "4. Management case",
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 30,
    },
    {
        "section_name": "Funding Required",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
        "form_name": "funding-required",
    },
    {
        "section_name": "Feasibility",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
        "form_name": "feasibility",
    },
    {
        "section_name": "Risk",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
        "form_name": "risk",
    },
    {
        "section_name": "Project Costs",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.4",
        "form_name": "project-costs",
    },
    {
        "section_name": "Skills And Resources",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.5",
        "form_name": "skills-and-resources",
    },
    {
        "section_name": "Community Representation",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.6",
        "form_name": "community-representation",
    },
    {
        "section_name": "Inclusiveness And Integration",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.7",
        "form_name": "inclusiveness-and-integration",
    },
    {
        "section_name": "Upload Business Plan",
        "tree_path": f"{APPLICATION_BASE_PATH}.4.8",
        "form_name": "upload-business-plan",
    },
    {
        "section_name": "5. Potential to deliver community benefits",
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "weighting": 30,
    },
    {
        "section_name": "Community Benefits",
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
        "form_name": "community-benefits",
    },
    {
        "section_name": "6. Added value to community",
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
        "weighting": 10,
    },
    {
        "section_name": "Value To The Community",
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
        "form_name": "value-to-the-community",
    },
    {
        "section_name": "7. Subsidy control / state aid",
        "tree_path": f"{APPLICATION_BASE_PATH}.7",
    },
    {
        "section_name": "Project Qualification",
        "tree_path": f"{APPLICATION_BASE_PATH}.7.1",
        "form_name": "project-qualification",
    },
    {
        "section_name": "8. Check declarations",
        "tree_path": f"{APPLICATION_BASE_PATH}.8",
    },
    {
        "section_name": "Declarations",
        "tree_path": f"{APPLICATION_BASE_PATH}.8.1",
        "form_name": "declarations",
    },
]
