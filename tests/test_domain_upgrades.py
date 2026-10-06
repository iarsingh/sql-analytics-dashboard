import pytest
from fastapi.testclient import TestClient
from sqldash.main import app

client = TestClient(app)


def test_ambiguous_questions_are_rejected():
    assert client.post("/generate", json={"question": "revenue and tickets"}).status_code == 422


def test_keyword_boundaries_do_not_match_larger_words():
    r = client.post("/generate", json={"question": "revenue altered yesterday"})
    assert r.status_code == 200
    assert r.json()["template"] == "revenue" and r.json()["executed"] is False
    assert client.post("/generate", json={"question": "pretickets"}).status_code == 422


def test_templates_are_discoverable_and_not_executed():
    r = client.get("/templates").json()
    assert {x["name"] for x in r["templates"]} == {"revenue", "tickets"}
    assert r["executed"] is False
