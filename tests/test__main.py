import json

from fastapi.testclient import TestClient

from main import app
from settings.settings import load_config

config = load_config('.env')

client = TestClient(app)


def test__create_source__success(db):
    response = client.post("/source", json={"secret": config.misc.secret})
    assert response.status_code == 202


def test__create_source__failed(db):
    response = client.post("/source", json={"secret": config.misc.secret[-1]})

    assert response.status_code == 403


def test__log_creation(db):
    response = client.post("/source", json={"secret": config.misc.secret})
    token = json.loads(response.content)
    data = json.dumps({"test": "this is a test data"})
    response = client.post("/log", json={"token": token['token'], "data": data})
    assert response.status_code == 200
