from bs4 import BeautifulSoup

from config import Config


def test_404(client):
    response = client.get("not_found")

    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert len(soup.find_all("a", href=Config.SUPPORT_DESK_APPLY)) == 1
