# -*- coding: utf-8 -*-
import os
import mock

from .config import configure_app, get_config_value


def test_configure_app(empty_app):
    configure_app(empty_app)
    assert empty_app["config"]
    expected_keys = {
        "host": "0.0.0.0",
        "port": "8000",
        "top": 5,
        "use_persistence": False,
        "db_host": "0.0.0.0",
        "db_port": "27017",
        "db_user": "autocomplete",
        "db_password": "autocomplete",
    }
    for key, value in expected_keys.items():
        assert empty_app["config"][key] == value

@mock.patch.dict(os.environ,{"HOST": "127.0.0.1"})
def test_get_config_value():
    assert get_config_value("HOST", "") == "127.0.0.1"
    assert get_config_value("HOST_TEST", "1.2.3.4") == "1.2.3.4"
