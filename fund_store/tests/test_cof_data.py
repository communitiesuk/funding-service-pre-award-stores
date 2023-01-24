from core.rounds import get_round, get_rounds_for_fund
from fsd_utils.config.commonconfig import CommonConfig

class MockRequest_cy:

    args = {
        "language": "cy"
    }


class MockRequest_en:

    args = {
        "language": "en"
    }

def test_get_cof_r2w3(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_en(),
    )
    result = get_round(CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_W3_ID)
    assert "Round 2 Window 3" == result[0]["title"]
    assert "Monday to Friday" == result[0]["support_availability"]["days"]


def test_get_cof_r2w3_welsh(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_cy(),
    )
    result = get_round(CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_W3_ID)
    assert "Cylch 2 Window 3" == result[0]["title"]
    assert "Monday to Friday" == result[0]["support_availability"]["days"]

def test_get_cof_r2w2(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_en(),
    )
    result = get_round(CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_ID)
    assert "Round 2 Window 2" == result[0]["title"]
    assert "Monday to Friday" == result[0]["support_availability"]["days"]


def test_get_cof(mocker, monkeypatch):

    monkeypatch.setattr(
        "core.rounds.request",
        MockRequest_en(),
    )
    result = get_rounds_for_fund(CommonConfig.COF_FUND_ID)
    assert 2 == len(result[0])
    assert "Round 2 Window 3" == result[0][1]["title"]
    assert "Round 2 Window 2" == result[0][0]["title"]