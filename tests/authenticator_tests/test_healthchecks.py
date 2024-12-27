import pytest


@pytest.mark.app(debug=False)
def test_app(app):
    assert not app.debug, "Ensure the app not in debug mode"


class TestHealthchecks:
    @pytest.mark.usefixtures("mock_redis_magic_links")
    def testChecks(self, authenticator_test_client):
        response = authenticator_test_client.get("/healthcheck")
        expected_dict = {
            "checks": [{"check_flask_running": "OK"}, {"check_db": "OK"}, {"check_redis": "OK"}],
            "version": "123123",
        }
        assert response.status_code == 200, "Unexpected response code"
        assert response.json == expected_dict, "Unexpected json body"
