import pytest

from settings.settings import load_config


@pytest.fixture(scope='session')
def db():
    config = load_config('.env')
