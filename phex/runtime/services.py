import asyncio
import importlib
import logging
import types
import typing

from phex.runtime import registry

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

    services: list[tuple[Service, ServiceConfig]] = []
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
        registry.register(service_config.id, service)
    return [service for service, _ in services]


async def bootstrap(
    bootstrappable: Bootstrappable, suppress_errors: bool = False
) -> typing.Any:
    return await _call(bootstrappable, "bootstrap", suppress_errors)


async def run(runnable: Runnable, suppress_errors: bool = False) -> typing.Any:
    return await _call(runnable, "run", suppress_errors)


async def dispose(
    disposable: Disposable, suppress_errors: bool = False
) -> typing.Any:  # noqa: E501
    return await _call(disposable, "dispose", suppress_errors)


async def _call(
    service: Service, function: str, suppress_errors: bool, *args, **kwargs
) -> typing.Any:  # noqa: E501
    service_module_name = getattr(service, "__name__")
    if not hasattr(service, function):
        raise AttributeError(
            "'{}' doesn't exist at {}".format(function, service_module_name)
        )
    try:
        callable = getattr(service, function)
        _logger.debug(
            "Calling '{}' of '{}'".format(function, service_module_name)
        )  # noqa: E501
        if asyncio.iscoroutinefunction(callable):
            result = await callable(*args, **kwargs)
        else:
            result = callable(*args, **kwargs)
        if result is not None:
            _logger.debug(
                "Called '{}' of '{}' with result '{}'".format(
                    function, service_module_name, repr(result)
                )
            )
        else:
            _logger.debug(
                "Called '{}' of '{}'".format(function, service_module_name)
            )  # noqa: E501
        return result
    except Exception as exc:
        if suppress_errors:
            _logger.error(
                "Failed calling '{}' of '{}': {}".format(
                    function, service_module_name, exc
                ),  # noqa: E501
                exc_info=True,
            )
            return
        raise
