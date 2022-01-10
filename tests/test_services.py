import os

import pytest
from phex.runtime import configuration, registry, services
from phex.runtime.protocol import ServiceConfig
from pytest_mock import MockerFixture

os.environ["PHEX_CONFIG"] = "./tests/config/phex.yaml"


@pytest.mark.asyncio
async def test_load_service():
    loaded_services = await services.load(
        [ServiceConfig(**service) for service in configuration.get().services],
        configuration.get(),
    )
    from tests.services import test_async, test_sync

    assert loaded_services[0] is test_sync
    assert loaded_services[1] is test_async
    assert registry.get("test_sync") is test_sync
    assert registry.get("test_async") is test_async


@pytest.mark.asyncio
async def test_bootstrap_service(mocker: MockerFixture):
    from tests.services import test_async, test_sync

    bootstrap_mock = mocker.patch.object(
        test_sync, "bootstrap", return_value="sync_result", autospec=True
    )
    sync_result = await services.bootstrap(test_sync)
    bootstrap_mock.assert_called_once()
    assert sync_result == "sync_result"

    bootstrap_mock = mocker.patch.object(
        test_async, "bootstrap", return_value="async_result", autospec=True
    )
    async_result = await services.bootstrap(test_async)
    bootstrap_mock.assert_called_once()
    assert async_result == "async_result"


@pytest.mark.asyncio
async def test_run_service(mocker: MockerFixture):
    from tests.services import test_async, test_sync

    run_mock = mocker.patch.object(
        test_sync, "run", return_value="sync_result", autospec=True
    )
    sync_result = await services.run(test_sync)
    run_mock.assert_called_once()
    assert sync_result == "sync_result"

    run_mock = mocker.patch.object(
        test_async, "run", return_value="async_result", autospec=True
    )
    async_result = await services.run(test_async)
    run_mock.assert_called_once()
    assert async_result == "async_result"


@pytest.mark.asyncio
async def test_dispose_service(mocker: MockerFixture):
    from tests.services import test_async, test_sync

    dispose_mock = mocker.patch.object(
        test_sync, "dispose", return_value="sync_result", autospec=True
    )
    sync_result = await services.dispose(test_sync)
    dispose_mock.assert_called_once()
    assert sync_result == "sync_result"

    dispose_mock = mocker.patch.object(
        test_async, "dispose", return_value="async_result", autospec=True
    )
    async_result = await services.dispose(test_async)
    dispose_mock.assert_called_once()
    assert async_result == "async_result"


@pytest.mark.asyncio
async def test_dispose_fail(mocker: MockerFixture):
    from tests.services import test_async, test_sync

    mocker.patch.object(
        test_sync, "dispose", side_effect=AssertionError(), autospec=True
    )
    with pytest.raises(AssertionError):
        await services.dispose(test_sync)
    await services.dispose(test_sync, True)

    mocker.patch.object(
        test_async, "dispose", side_effect=AssertionError(), autospec=True
    )
    with pytest.raises(AssertionError):
        await services.dispose(test_async)
    await services.dispose(test_async, True)


@pytest.mark.asyncio
async def test_call_missing_function(mocker: MockerFixture):
    from tests.services import test_async, test_sync

    with pytest.raises(AttributeError):
        await services._call(test_sync, "unavailable", False)
    with pytest.raises(AttributeError):
        await services._call(test_sync, "unavailable", True)

    with pytest.raises(AttributeError):
        await services._call(test_async, "unavailable", False)
    with pytest.raises(AttributeError):
        await services._call(test_async, "unavailable", True)
