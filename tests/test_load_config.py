import os

import pytest
from phex.runtime import configuration

os.environ["PHEX_CONFIG"] = "./tests/config/phex.yaml"
configuration.get.cache_clear()


def test_config_load():
    assert configuration.get() is not None
    assert configuration.get() is configuration.get()
    assert configuration.get().testing
    assert configuration.get.cache_info().hits >= 3


def test_config_cannot_change():
    with pytest.raises(AttributeError):
        configuration.get().unavailable
