import httpx

def test_sample_api():
    response = httpx.get("https://api.github.com")
    assert response.status_code == 200
