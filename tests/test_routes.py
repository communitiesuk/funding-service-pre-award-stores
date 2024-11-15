def test_test_route(flask_test_client):
    response = flask_test_client.get("/test")

    assert 200 == response.status_code, "Unexpected status code"
    assert "Consolidation is back on the menu!" == response.json(), "Unexpected json body"
