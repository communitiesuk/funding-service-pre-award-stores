LOADER_CONFIG = {
    "sections_config": [
        {
            "section_name": {
                "en": "1. Expression of interest",
                "cy": "1. Mynegi diddordeb",
            },
            "tree_path": "1037.1.1",
            "requires_feedback": True,
        },
        {
            "section_name": {
                "en": "1.1 Organisation details",
                "cy": "1.1 Manylion y sefydliad",
            },
            "tree_path": "1037.1.1.1",
            "form_name_json": {
                "en": "organisation-details-25",
                "cy": "manylion-y-sefydliad-25",
            },
        },
        {
            "section_name": {
                "en": "1.2 About your asset",
                "cy": "1.2 Ynglŷn â'ch ased",
            },
            "tree_path": "1037.1.1.2",
            "form_name_json": {
                "en": "about-your-asset-25",
                "cy": "ynglyn-ach-ased-25",
            },
        },
        {
            "section_name": {
                "en": "1.3 Your funding request",
                "cy": "1.3 Eich cais am gyllid",
            },
            "tree_path": "1037.1.1.3",
            "form_name_json": {
                "en": "your-funding-request-25",
                "cy": "eich-cais-am-gyllid-25",
            },
        },
        {
            "section_name": {
                "en": "1.4 Development support provider (not scored)",
                "cy": "1.4 Darparwr cymorth datblygu (heb ei sgorio)",
            },
            "tree_path": "1037.1.1.4",
            "form_name_json": {
                "en": "development-support-provider-25",
                "cy": "darparwr-cymorth-datblygu-25",
            },
        },
        {
            "section_name": {
                "en": "1.5 Declaration",
                "cy": "1.5 Datganiad",
            },
            "tree_path": "1037.1.1.5",
            "form_name_json": {
                "en": "declaration-25",
                "cy": "datganiad-25",
            },
        },
    ],
    "fund_config": {
        "id": "4db6072c-4657-458d-9f57-9ca59638317b",
        "short_name": "COF25-EOI",
        "welsh_available": True,
        "owner_organisation_name": "Ministry of Housing, Communities and Local Government",
        "owner_organisation_shortname": "MHCLG",
        "owner_organisation_logo_uri": None,
        "funding_type": "EOI",
        "name_json": {"en": "Community Ownership Fund 2025", "cy": "Y Cronfa Perchnogaeth Gymunedol 2025"},
        "title_json": {
            "en": "expression of interest in applying for the Community Ownership Fund 2025",
            "cy": "Gwneud cais am ddatganiad o ddiddordeb mewn gwneud cais i'r Gronfa Perchnogaeth Gymunedol",
        },
        "description_json": {
            "en": "The Community Ownership Fund is a £150 million fund over 4 years to support community groups across England, Wales, Scotland and Northern Ireland to take ownership of assets which are at risk of being lost to the community.",
            "cy": (  # TODO: Provide welsh translation
                "The Community Ownership Fund is a £150 million fund over 4 years"
                " to support community groups across England, Wales, Scotland and"
                " Northern Ireland to take ownership of assets which are at risk"
                " of being lost to the community."
            ),
        },
    },
    "round_config": {
        "id": "9104d809-0fb0-4144-b514-55e81cc2b6fa",
        "fund_id": "4db6072c-4657-458d-9f57-9ca59638317b",
        "short_name": "R1",
        "opens": "2024-10-30T11:59:00",
        "assessment_start": "2024-10-30T09:00:00",
        "deadline": "2024-12-11T14:00:00",
        "application_reminder_sent": False,
        "reminder_date": "2024-12-01T11:59:00",
        "assessment_deadline": "2025-01-31T17:00:00",
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus/community-ownership-fund-2025-prospectus",
        "privacy_notice": "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/community-ownership-fund-privacy-notice",
        "reference_contact_page_over_email": True,
        "contact_email": "COF@communities.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions_json": {
            "en": "You must complete this Expression of Interest (EOI) form if you are interested in applying for the Community Ownership Fund 2025 (COF25).",
            "cy": (
                "Mae'n rhaid i chi gwblhau'r ffurflen Datganiad o Ddiddordeb hon os"
                " oes diddordeb gennych mewn gwneud cais i'r Gronfa Perchnogaeth Gymunedol 2025."
            ),
        },
        "feedback_link": "https://www.gov.uk/government/organisations/ministry-of-housing-communities-local-government",
        "project_name_field_id": "SMRWjl",
        "application_guidance_json": {"en": "", "cy": ""},
        "guidance_url": "https://www.gov.uk/government/organisations/ministry-of-housing-communities-local-government",
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": True,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": False,
        "is_expression_of_interest": True,
        "eoi_decision_schema": None,
        "feedback_survey_config": {
            "has_feedback_survey": False,
            "has_section_feedback": True,
            "is_feedback_survey_optional": False,
            "is_section_feedback_optional": True,
        },
        "eligibility_config": {"has_eligibility": False},
        "title_json": {"en": "Round 1", "cy": "Rownd 1"},
        "contact_us_banner_json": {
            "en": '<h2 class="govuk-heading-m">Get application support</h2>\r\n                 <p class="govuk-body">\r\n                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Visit the My Community website</a>\r\n                    for information and guidance on applying to Community Ownership Fund 2025.\r\n                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Fill out the enquiry form</a>\r\n                    to request advice from My Community.\r\n                </p>\r\n                <p class="govuk-body">\r\n                    We cannot provide direct support to applicants outside of this service.\r\n                </p>\r\n                <h2 class="govuk-heading-m">Get technical support</h2>\r\n                <p  class="govuk-body">\r\n                    Contact the Ministry of Housing, Communities & Local Government funding team if you need\r\n                    help with accessing or submitting an application form.\r\n                </p>',
            "cy": """
                 <h2 class="govuk-heading-m">Cael cymorth â'r cais</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Ewch i wefan My Community</a>
                    i gael gwybodaeth ac arweiniad ar wneud cais i'r Gronfa Perchnogaeth Gymunedol 2025.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Llenwch y ffurflen ymholiad</a>
                    i ofyn am gyngor gan My Community.
                </p>
                <p class="govuk-body">
                    Ni allwn ddarparu cymorth uniongyrchol i ymgeiswyr tu hwnt i'r gwasanaeth hwn.
                </p>
                <h2 class="govuk-heading-m">Cael cymorth technegol</h2>
                <p  class="govuk-body">
                    Cysylltwch â thîm cyllid yr Adran Ffyniant Bro, Tai a Chymunedau os oes angen help arnoch i gael at ffurflen gais neu ei chyflwyno.
                </p>
            """,
        },
    },
    "base_path": 1037,
}
