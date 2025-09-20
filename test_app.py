import pytest
import json
from app import app, NOTES_FILE, write_notes

@pytest.fixture
def client(tmp_path, monkeypatch):
    """Use a temporary notes.json file for tests"""
    test_notes_file = tmp_path / "notes.json"
    test_notes_file.write_text("[]", encoding="utf-8")

    monkeypatch.setattr("app.NOTES_FILE", str(test_notes_file))
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "UP"}

def test_index_serves_html(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<html" in rv.data.lower()

def test_notes_crud(client):
    # initially empty
    rv = client.get("/api/notes")
    assert rv.status_code == 200
    assert rv.get_json() == []

    # create note
    note = {"id": "n1", "title": "Test", "body": "Hello"}
    rv = client.post("/api/notes", json=note)
    assert rv.status_code == 201
    assert rv.get_json()["id"] == "n1"

    # list again
    rv = client.get("/api/notes")
    data = rv.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Test"

    # get single note
    rv = client.get("/api/notes/n1")
    assert rv.status_code == 200
    assert rv.get_json()["title"] == "Test"

    # update note
    updated = {"id": "n1", "title": "Updated Title", "body": "Hello"}
    rv = client.put("/api/notes/n1", json=updated)
    assert rv.status_code == 200
    assert rv.get_json()["title"] == "Updated Title"

    # delete note
    rv = client.delete("/api/notes/n1")
    assert rv.status_code == 200
    assert rv.get_json()["deleted"] == "n1"

    # ensure empty again
    rv = client.get("/api/notes")
    assert rv.get_json() == []
