import asyncio
import importlib
import logging
import types
import typing

from .configuration import Configuration
from .protocol import Initializable  # noqa: E501
from .protocol import Bootstrappable, Disposable, Runnable, ServiceConfig

_logger = logging.getLogger(__name__)

Service = typing.Union[
    types.ModuleType, Initializable, Bootstrappable, Runnable, Disposable
]  # noqa: E501


async def load(
    service_configs: list[ServiceConfig],
    configuration: Configuration,
    *args,
    suppress_errors: bool = False,
    **kwargs
) -> list[Service]:

    services: list[tuple[typing.Any, typing.Any]] = []
    for service_config in service_configs:
        service = importlib.import_module(service_config.module)
        services.append((service, service_config))
    await asyncio.gather(
        *[
            _call(
                service,
                "initialize",
                suppress_errors,
                configuration,
                *args,
                **kwargs  # noqa: E501
            )
            for service, _ in services
        ]
    )
    for service, service_config in services:
        pass
    return [service for service, _ in services]


async def bootstrap(bootstrappable: Service, suppress_errors: bool = False):
    return await _call(bootstrappable, "bootstrap", suppress_errors)


async def run(runnable: Service, suppress_errors: bool = False):
    return await _call(runnable, "run", suppress_errors)


async def dispose(disposable: Service, suppress_errors: bool = False):
    return await _call(disposable, "dispose", suppress_errors)


async def _call(
    service: Service, name: str, suppress_errors: bool, *args, **kwargs
):  # noqa: E501
    service_name = getattr(service, "__name__")
    try:
        if hasattr(service, name):
            callable = getattr(service, name)
            _logger.debug("Calling '{}' of '{}'".format(name, service_name))
            if asyncio.iscoroutinefunction(callable):
                result = await callable(*args, **kwargs)
            else:
                result = callable(*args, **kwargs)
            if result is not None:
                _logger.debug(
                    "Called '{}' of '{}' with result '{}'".format(
                        name, service_name, repr(result)
                    )
                )
            else:
                _logger.debug(
                    "Called '{}' of '{}'".format(name, service_name)
                )  # noqa: E501
            return result
    except Exception as exc:
        if suppress_errors:
            _logger.error(
                "Failed calling '{}' of '{}': {}".format(
                    name, service_name, exc
                ),  # noqa: E501
                exc_info=True,
            )
            return
        raise
