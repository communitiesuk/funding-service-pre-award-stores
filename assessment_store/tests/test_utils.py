from unittest import mock

from api.routes.scores_justifications import utils
from tests.mocks.mock_round_store import mock_get_round_just_weightings
from tests.mocks.mock_round_store import STRATEGIC_CASE_ID


class Test_Utils:
    def test_calc_weights_by_id(self):
        with mock.patch(
            "api.routes.scores_justifications.utils.get_round_json",
            return_value=mock_get_round_just_weightings(),
        ) as mock_get_round_json_func:
            result = utils.calc_weighted_scores_for_criteria(
                fund_id="fund_1",
                round_id="round_1",
                crit_id=STRATEGIC_CASE_ID,
                crit_name="Strategic Case",
                list_of_scores=[4, 6],
                query_by_name=False,
            )
            mock_get_round_json_func.assert_called_once_with(
                "fund_1", "round_1"
            )

            assert 10 == result["total_score"], "Wrong total score"
            assert 8 == result["weighted_score"], "Wrong weighted score"
            assert 0.8 == result["weight"]

    def test_calc_weights_by_name(self):
        with mock.patch(
            "api.routes.scores_justifications.utils.get_round_json",
            return_value=mock_get_round_just_weightings(),
        ) as mock_get_round_json_func:
            result = utils.calc_weighted_scores_for_criteria(
                fund_id="fund_1",
                round_id="round_1",
                crit_id=STRATEGIC_CASE_ID,
                crit_name="Strategic case",
                list_of_scores=[12, 8],
                query_by_name=True,
            )
            mock_get_round_json_func.assert_called_once_with(
                "fund_1", "round_1"
            )
            assert 20 == result["total_score"], "Wrong total score"
            assert 16 == result["weighted_score"], "Wrong weighted score"
            assert 0.8 == result["weight"]
