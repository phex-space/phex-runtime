import pytest
from phex.runtime import configuration, services
from phex.runtime.protocol import ServiceConfig
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_load_service():
    loaded_services = await services.load(
        [
            ServiceConfig("test_sync", "tests.services.test_sync"),
            ServiceConfig("test_async", "tests.services.test_async"),
        ],
        configuration.get(),
    )
    from tests.services import test_async, test_sync

    assert loaded_services[0] is test_sync
    assert loaded_services[1] is test_async


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
