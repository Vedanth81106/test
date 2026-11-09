from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_hello_world():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"Hello": "World"}


def test_root_rejects_unsupported_method():
    response = client.post("/")

    assert response.status_code == 405


def test_read_item_returns_item_id_and_query():
    response = client.get("/items/42", params={"q": "search"})

    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "search"}


def test_read_item_returns_null_query_when_omitted():
    response = client.get("/items/7")

    assert response.status_code == 200
    assert response.json() == {"item_id": 7, "q": None}


def test_read_item_rejects_non_integer_id():
    response = client.get("/items/not-a-number")

    assert response.status_code == 422
