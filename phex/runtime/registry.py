import typing


_map = {}


def register(id_: str, item: typing.Any) -> None:
    if id_ in _map:
        raise KeyError("item is already registered for the given id")
    _map[id_] = item


def get(id_: str) -> typing.Any:
    if id_ not in _map:
        raise KeyError("no item is registered for the the given id")
    return _map[id_]
