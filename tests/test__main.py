import json

import pytest
from fastapi.testclient import TestClient

from db.logger_db import Source, Log
from db.models_management import get
from main import app
from settings.settings import load_config

config = load_config('.env')

client = TestClient(app)


def test__create_source__success(db):
    first_response = client.post("/source", json={"secret": config.misc.secret})
    assert first_response.status_code == 202
    second_response = client.post("/source", json={"secret": config.misc.secret})
    assert second_response.status_code == 202
    assert eval(second_response.content)["token"] == eval(first_response.content)["token"]


def test__create_source__failed(db):
    response = client.post("/source", json={"secret": config.misc.secret[-1]})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test__log_creation(db):
    response = client.post("/source", json={"secret": config.misc.secret})
    token = json.loads(response.content)
    data = json.dumps({"test": "this is a test data"})
    response = client.post("/log", json={"message": data, "token": token['token'], "level": "debug"})
    assert response.status_code == 202
