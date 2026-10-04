from fastapi.testclient import TestClient
from sqldash.main import app

client = TestClient(app)


def test_select_and_refuse_write():
    payload = client.post("/generate", json={"question": 'revenue by region'}).json()
    assert "SUM(revenue)" in payload["sql"]
    assert payload["read_only"] is True
    assert client.post("/generate", json={"question": "delete old rows"}).status_code == 422
