
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
    response = client.post(url="/patient/", json={"name": "sad", "surename": "sada"})
    assert response.status_code == 200
    assert  {"name": "sad", "surename": "sada"} in response.json().values()


def test_pk_patient():
    response = client.get("/patient/1")
    assert response.status_code in [200, 204]

