from phex_runtime import configuration


def test_config_load():
    assert configuration.get() is not None
    assert configuration.get() is configuration.get()
