import pytest

from phex.runtime import configuration

@pytest.fixture(autouse=True)
def reset_before_each():
    configuration.get.cache_clear
