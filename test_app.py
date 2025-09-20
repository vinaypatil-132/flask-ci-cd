from app import app

def test_home():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert "Hello from NEW version 2.0 🚀" in r.data.decode("utf-8")

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json.get("status") == "UP"
