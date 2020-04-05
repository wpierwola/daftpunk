
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


def test_get_method():
    response = client.get("/method/")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_post_method():
    response = client.post("/method/")
    assert response.status_code == 200
    assert response.json() == {"method": "POST"}


def test_put_method():
    response = client.put("/method/")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}


def test_delete_method():
    response = client.delete("/method/")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


def test_add_patient():
    param_grid = {"Anna": "Kowalska",
                "asdmad": "oijppom",
                "rweeawdas": "pokomjoij"}

    for name, surname in param_grid.items():
        response = client.post("/patient", params={name: surname})
        assert response.status_code == 200
        assert response.json()["patient"] == {"name":name, "surename":surname}

