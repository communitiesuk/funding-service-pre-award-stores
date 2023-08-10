from config.fund_loader_config.logo import DLUHC_LOGO_PNG

fund_config = {
    "id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
    "name_json": {
        "en": "Community Ownership Fund",
        "cy": "Y Cronfa Perchnogaeth Gymunedol",
    },
    "title_json": {
        "en": "funding to save an asset in your community",
        "cy": "gyllid i achub ased yn eich cymuned",
    },
    "short_name": "COF",
    "description_json": {
        "en": (
            "The Community Ownership Fund is a £150 million fund over 4 years"
            " to support community groups across England, Wales, Scotland and"
            " Northern Ireland to take ownership of assets which are at risk"
            " of being lost to the community."
        ),
        "cy": (  # TODO: Provide welsh translation
            "The Community Ownership Fund is a £150 million fund over 4 years"
            " to support community groups across England, Wales, Scotland and"
            " Northern Ireland to take ownership of assets which are at risk"
            " of being lost to the community."
        ),
    },
    "welsh_available": True,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

COF_APPLICATION_GUIDANCE = (  # TODO: Provide welsh translation
    "<h2 class='govuk-heading govuk-heading-s'>What we'll ask you for</h2><p"
    " class='govuk-body'>You can preview the <a href='{all_questions_url}'>full list of"
    " application questions</a>.</p><p class='govuk-body'>We'll also ask you to upload"
    " a business plan to support the answers you've given us in the management case"
    " section.</p>"
)
