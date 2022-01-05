import dataclasses
import functools


@dataclasses.dataclass
class Configuration:
    pass


@functools.lru_cache(1)
def get() -> Configuration:
    return Configuration()
