from unittest.mock import Mock

import pytest
from api.routes.subcriterias.get_sub_criteria import (
    sort_add_another_component_contents,
)


@pytest.mark.parametrize(
    "answer_from_form_runner, expected_description, expected_amount",
    [
        (
            ["An Answer : £1"],
            ["An Answer "],
            ["£1"],
        ),
        (
            ["An Answer : with colon : £1"],
            ["An Answer : with colon "],
            ["£1"],
        ),
        (
            ["An : Answer : with : lots: of :colons : £1"],
            ["An : Answer : with : lots: of :colons "],
            ["£1"],
        ),
        (
            ["An Answer : £1", "Another Answer : £2"],
            ["An Answer ", "Another Answer "],
            ["£1", "£2"],
        ),
    ],
)
def test_sort_add_another_component_contents(
    answer_from_form_runner,
    expected_description,
    expected_amount,
):
    themes_answers = [
        {
            "presentation_type": "heading",
            "question": "Test Heading",
            "field_id": "123",
            "answer": "Test Heading",
        },
        {
            "presentation_type": "description",
            "question": "Test Description",
            "field_id": "123",
            "answer": answer_from_form_runner,
        },
        {
            "presentation_type": "amount",
            "question": "Test Amount",
            "field_id": "123",
            "answer": answer_from_form_runner,
        },
    ]

    sort_add_another_component_contents(themes_answers)

    assert themes_answers[0]["answer"] == "Test Heading"
    assert themes_answers[1]["answer"] == expected_description
    assert themes_answers[2]["answer"] == expected_amount


def test_sort_add_another_component_contents_log_when_no_answer(monkeypatch):
    current_app = Mock()
    monkeypatch.setattr(
        "api.routes.subcriterias.get_sub_criteria.current_app", current_app
    )

    themes_answers = [
        {
            "presentation_type": "heading",
            "question": "Test Heading",
            "field_id": "123",
        },
        {
            "presentation_type": "description",
            "question": "Test Description",
            "field_id": "123",
        },
        {
            "presentation_type": "amount",
            "question": "Test Amount",
            "field_id": "123",
        },
    ]

    sort_add_another_component_contents(themes_answers)

    current_app.logger.debug.assert_called_with(
        "Answer not provided for field_id: 123"
    )
