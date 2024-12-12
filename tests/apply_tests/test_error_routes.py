from bs4 import BeautifulSoup


def test_404(client):
    response = client.get("not_found")

    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    link = soup.find("a", href="https://mhclgdigital.atlassian.net/servicedesk/customer/portal/5/group/68")
    assert link is not None
