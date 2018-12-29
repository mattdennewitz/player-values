import json

import pytest

from models import Config


@pytest.fixture
def app_config():
    schema = Config()
    config_data = json.load(open('league_config.json'))
    return schema.load(config_data)
