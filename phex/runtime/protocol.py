import dataclasses
import typing

from phex.runtime.configuration import Configuration


class Initializable(typing.Protocol):
    async def initialize(self, config: Configuration, *args, **kwargs) -> None:
        """Initializes the corresponding parent"""


class Bootstrappable(typing.Protocol):
    async def bootstrap(self) -> None:
        """Bootstraps the corresponding parent"""


class Runnable(typing.Protocol):
    async def run(self) -> None:
        """Runs the corresponding parent"""


class Disposable(typing.Protocol):
    async def dispose(self) -> None:
        """Disposes the corresponding parent"""


@dataclasses.dataclass
class ServiceConfig:
    id: str
    module: str
