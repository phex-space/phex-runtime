import functools
import os

import yaml


class Configuration(dict):
    def __init__(self, initial_data: dict):
        super().__init__(initial_data)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)


@functools.lru_cache(1)
def get() -> Configuration:
    try:
        from yaml import CLoader as Loader
    except ImportError:  # pragma: no cover
        from yaml import Loader
    configuration_file = os.environ.get(
        "PHEX_CONFIG", os.path.join(os.getcwd(), "phex.yaml")
    )
    with open(configuration_file, "r") as fp:
        return Configuration(yaml.load(fp, Loader=Loader))
