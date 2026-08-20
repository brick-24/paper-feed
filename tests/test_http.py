import requests

def test_http():
    response = requests.get("https://google.com/")
    assert response.status_code == 200
