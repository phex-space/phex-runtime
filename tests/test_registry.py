import pytest

from phex.runtime import registry


def test_register_get():
    registry.register("test_constant", 42)
    assert registry.get("test_constant") == 42


def test_fail_by_missing_id():
    with pytest.raises(KeyError):
        registry.get("missing_key")


def test_fail_by_existing_id():
    registry.register("already", "there")
    with pytest.raises(KeyError):
        registry.register("already", "there")
