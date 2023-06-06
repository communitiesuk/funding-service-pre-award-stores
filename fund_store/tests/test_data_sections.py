from typing import List

import pytest
from config.fund_loader_config.cof.deprecated_fund_config.assessment_section_config import (
    scored_sections,
)
from config.fund_loader_config.cof.deprecated_fund_config.assessment_section_config import (
    unscored_sections,
)
from config.fund_loader_config.cof.deprecated_fund_config.cof_form_config import (
    COF_R2_ORDERED_FORMS_CONFIG,
)
from config.fund_loader_config.cof.deprecated_fund_config.sort_application_sections import (
    return_numerically_sorted_section_for_application,
)
from config.fund_loader_config.cof.deprecated_fund_config.sort_assessment_sections import (
    return_numerically_sorted_section_for_assessment,
)
from db.models.section import Section
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import insert_application_sections
from db.queries import insert_assessment_sections
from db.queries import upsert_fields
from fsd_test_utils.test_config.useful_config import UsefulConfig


def test_get_application_sections(seed_dynamic_data):
    sections: List[Section] = get_application_sections_for_round(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )
    assert len(sections) == 3
    first, second, third = sections
    assert first.title_json == {"en": "Middle1"}
    assert len(first.children) == 1
    assert second.title_json == {"en": "Middle2"}
    assert len(second.children) == 1
    assert third.title_json == {"en": "skills"}
    assert len(third.children) == 0


def test_get_assessment_sections(seed_dynamic_data):
    sections: List[Section] = get_assessment_sections_for_round(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
        "",
    )
    assert len(sections) == 1
    assert sections[0].title_json == {"en": "assess section 1"}
    assert len(sections[0].children) == 1
    assert sections[0].children[0].title_json == {"en": "assess section 1 a"}
    assert len(sections[0].children[0].children) == 0


def test_load_application_sections(seed_dynamic_data):
    sorted_application_sections = return_numerically_sorted_section_for_application(
        COF_R2_ORDERED_FORMS_CONFIG, "0.1"
    )["sorted_sections"]
    result = insert_application_sections(
        seed_dynamic_data["funds"][0]["rounds"][0]["id"], sorted_application_sections
    )
    assert len(result) == 28


@pytest.mark.skip(reason="not implemented assessment loading yet")
def test_load_assessment_sections():
    # input config
    assessment_config = return_numerically_sorted_section_for_assessment(
        scored_sections, unscored_sections
    )

    inserted_field_ids = upsert_fields(assessment_config["all_fields"])
    result = insert_assessment_sections(UsefulConfig.COF_ROUND_2_ID, assessment_config)

    assert len(inserted_field_ids) == 124
    assert len(result["inserted_sections"]) == 53
    assert len(result["inserted_section_field_links"]) == 124
