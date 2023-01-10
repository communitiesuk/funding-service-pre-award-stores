from unittest.mock import Mock

from api.routes.subcriterias.get_sub_criteria import (
    sort_add_another_component_contents,
)


def test_sort_add_another_component_contents():
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
            "answer": ["Test Description: Test"],
        },
        {
            "presentation_type": "amount",
            "question": "Test Amount",
            "field_id": "123",
            "answer": ["Test Amount: 100"],
        },
    ]

    sort_add_another_component_contents(themes_answers)

    assert themes_answers[0]["answer"] == "Test Heading"
    assert themes_answers[1]["answer"] == ["Test Description"]
    assert themes_answers[2]["answer"] == ["100"]


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
