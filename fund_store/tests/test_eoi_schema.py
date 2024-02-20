import json

import pytest
from config.fund_loader_config.cof.eoi_r1_schema import COF_PLANNING_PERMISSION_CAVEAT
from config.fund_loader_config.cof.eoi_r1_schema import COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT
from config.fund_loader_config.cof.eoi_r1_schema import COF_R3_EOI_SCHEMA
from config.fund_loader_config.cof.eoi_r1_schema import COF_SECURE_MATCH_FUNDING_CAVEAT
from fsd_utils import Eoi_Decision
from fsd_utils import evaluate_eoi_response


def test_eoi_schema_throws_no_errors_with_all_forms():
    with open("tests/test_data/cof_eoi.json", "r") as f:
        forms = json.loads(f.read())
    result = evaluate_eoi_response(schema=COF_R3_EOI_SCHEMA, forms=forms)

    assert result


@pytest.mark.parametrize(
    "question_key,supplied_answer,exp_decision,exp_caveats",
    [
        ("non-existant-question", "anything", Eoi_Decision.PASS, []),
        (
            "uYiLsv",
            "not-yet-incorporated",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [
                "Incorporate your organisation: You must have incorporated your"
                " organisation by the time you submit a full application. If you remain"
                " unincorporated, your application will be ineligible."
            ],
        ),
        ("NcQSbU", True, Eoi_Decision.FAIL, []),
        ("eEaDGz", False, Eoi_Decision.FAIL, []),
        ("zurxox", False, Eoi_Decision.FAIL, []),
        ("lLQmNb", False, Eoi_Decision.FAIL, []),
        ("fBhSNc", False, Eoi_Decision.FAIL, []),
        ("eOWKoO", False, Eoi_Decision.FAIL, []),
        ("foQgiy", False, Eoi_Decision.FAIL, []),
        (
            "XuAyrs",
            "Yes, a parish or community council",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA["XuAyrs"][0]["caveat"]],
        ),
        (
            "XuAyrs",
            "Yes, another type of public authority",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA["XuAyrs"][1]["caveat"]],
        ),
        (
            "nbLaHH",
            True,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA["nbLaHH"][0]["caveat"]],
        ),
        (
            "oblxxv",
            False,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA["oblxxv"][0]["caveat"]],
        ),
        (
            "kWRuac",
            "Not yet approached any funders",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT],
        ),
        (
            "kWRuac",
            "Approached some funders but not yet secured",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT],
        ),
        (
            "kWRuac",
            "Secured some match funding",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT],
        ),
        (
            "kWRuac",
            "Approached all funders but not yet secured",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT],
        ),
        (
            "yZxdeJ",
            True,
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA["yZxdeJ"][0]["caveat"]],
        ),
        (
            "UORyaF",
            "Not sure",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT],
        ),
        (
            "jICagT",
            "Not yet started",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_PLANNING_PERMISSION_CAVEAT],
        ),
        (
            "jICagT",
            "Early stage",
            Eoi_Decision.PASS_WITH_CAVEATS,
            [COF_PLANNING_PERMISSION_CAVEAT],
        ),
        ("fZAMFv", "2000001", Eoi_Decision.FAIL, []),
    ],
)
def test_answer_and_result(question_key, supplied_answer, exp_decision, exp_caveats):
    # Construct a dummy form with the supplied question and answer
    forms = [
        {
            "name": "COF EOI Test question",
            "questions": [
                {
                    "question": "Test question",
                    "fields": [
                        {
                            "key": question_key,
                            "title": "test question",
                            "type": "test",
                            "answer": supplied_answer,
                        }
                    ],
                }
            ],
        },
    ]
    # evaluate a response
    result = evaluate_eoi_response(schema=COF_R3_EOI_SCHEMA, forms=forms)

    assert result
    assert result["decision"] == exp_decision
    assert result["caveats"] == exp_caveats


@pytest.mark.parametrize("question_key", COF_R3_EOI_SCHEMA.keys())
def test_answers_with_non_conditioned_values(question_key):
    # Construct a dummy form with the supplied question and answer
    forms = [
        {
            "name": "COF EOI Test question",
            "questions": [
                {
                    "question": "Test question",
                    "fields": [
                        {
                            "key": question_key,
                            "title": "test question",
                            "type": "test",
                            "answer": "123",
                        }
                    ],
                }
            ],
        },
    ]
    # evaluate a response
    result = evaluate_eoi_response(schema=COF_R3_EOI_SCHEMA, forms=forms)

    assert result
    assert result["decision"] == Eoi_Decision.PASS
    assert result["caveats"] == []
