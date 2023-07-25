from fsd_test_utils.test_config.useful_config import UsefulConfig


def test_get_fund_by_id(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/123")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Fund Name 1"


def test_get_fund_by_short_name(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/ABC?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result["name"] == "Fund Name 1"


def test_get_round_by_short_name(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/FND1/rounds/RND1?use_short_name=True")
    assert response.status_code == 200
    result = response.json
    assert result["title"] == "Round 1"


def test_get_round_by_id(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds/FND1/rounds/RND1")
    assert response.status_code == 200
    result = response.json
    assert result["title"] == "Round 1"


def test_get_round_by_bad_id(flask_test_client, mocker):
    mocker.patch("api.routes.get_round_by_id", return_value=None)
    response = flask_test_client.get("/funds/FND1/rounds/RND1")
    assert response.status_code == 404


def test_get_all_funds(flask_test_client, mock_get_fund_round):
    response = flask_test_client.get("/funds")
    assert response.status_code == 200
    result = response.json
    assert result[0]["name"] == "Fund Name 1"


def test_get_all_funds_no_data(flask_test_client, mocker):
    mocker.patch("api.routes.get_all_funds", return_value=[])
    response = flask_test_client.get("/funds")
    assert response.status_code == 200


def test_get_app_sections_for_round(flask_test_client, mock_get_sections):
    response = flask_test_client.get(
        f"/funds/{UsefulConfig.COF_FUND_ID}/rounds/"
        f"{UsefulConfig.COF_ROUND_2_ID}/sections/application"
    )
    assert response.status_code == 200
    result = response.json
    assert result[0]["title"] == "Top"


def test_get_assess_sections_for_round(flask_test_client, mock_get_sections):
    response = flask_test_client.get(
        f"/funds/{UsefulConfig.COF_FUND_ID}/rounds/"
        f"{UsefulConfig.COF_ROUND_2_ID}/sections/assessment"
    )
    assert response.status_code == 200
    result = response.json
    assert result[0]["title"] == "Top"
