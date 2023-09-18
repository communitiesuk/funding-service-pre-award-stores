from typing import List

import pytest
from config.fund_loader_config.cof.cof_r2 import APPLICATION_BASE_PATH
from config.fund_loader_config.cof.cof_r2 import ASSESSMENT_BASE_PATH
from config.fund_loader_config.cof.cof_r2 import cof_r2_sections
from config.fund_loader_config.cof.cof_r2 import COF_ROUND_2_WINDOW_2_ID
from config.fund_loader_config.cof.cof_r2 import fund_config
from config.fund_loader_config.cof.cof_r2 import rounds_config
from db.models.section import Section
from db.queries import get_application_sections_for_round
from db.queries import get_assessment_sections_for_round
from db.queries import insert_base_sections
from db.queries import insert_fund_data
from db.queries import insert_or_update_application_sections
from db.queries import insert_round_data


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


def test_load_application_sections(clear_test_data):
    insert_fund_data(fund_config)
    insert_round_data(rounds_config)

    base_sections = insert_base_sections(
        APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, COF_ROUND_2_WINDOW_2_ID
    )
    application_sections = insert_or_update_application_sections(
        COF_ROUND_2_WINDOW_2_ID, cof_r2_sections
    )
    assert len(base_sections) == 2
    assert len(application_sections) == 28


@pytest.mark.skip(reason="not implemented assessment loading yet")
def test_load_assessment_sections():
    pass
