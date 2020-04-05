
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize("name", ['Zenek', 'Marek', 'Alojzy Niezdąży'])
def test_hello_name(name):
    # name = 'elo'
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {'msg': f"Hello {name}"}

