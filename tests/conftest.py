from asyncio import create_subprocess_exec, sleep
from collections.abc import AsyncIterator, Callable
from os import environ
from sys import executable
from typing import Literal

from httpx import ConnectError, get
from litestar import Litestar
from litestar.testing import AsyncTestClient
from nllb import AsyncTranslatorClient, TranslatorClient
from pytest import fixture

from server.app import app
from server.config import Config


def client_factory(config: Config, *, no_lifespans: bool) -> AsyncTestClient[Litestar]:
    litestar = app(config)

    if no_lifespans:
        litestar._lifespan_managers.clear()

    return AsyncTestClient(app=litestar, backend_options={"use_uvloop": True})


@fixture(scope="session")
def auth_token() -> str:
    return "test_token"


@fixture(scope="session", autouse=True)
def anyio_backend() -> tuple[Literal["asyncio", "trio"], dict[str, bool]]:
    return "asyncio", {"use_uvloop": True}


@fixture
async def client(auth_token: str) -> AsyncIterator[AsyncTestClient[Litestar]]:
    config = Config()
    config.auth_token = auth_token

    async with AsyncTestClient(app=app(config), backend_options={"use_uvloop": True}) as client:
        yield client


@fixture
async def client_factory_without_lifespans() -> Callable[[Config], AsyncTestClient[Litestar]]:
    return lambda config: client_factory(config, no_lifespans=True)


@fixture(scope="session")
async def session_client(auth_token: str) -> AsyncIterator[AsyncTestClient[Litestar]]:
    config = Config()
    config.auth_token = auth_token

    async with AsyncTestClient(app=app(config), backend_options={"use_uvloop": True}) as client:
        yield client


@fixture(scope="session")
async def app_url() -> AsyncIterator[str]:
    config = Config()
    url = f"http://localhost:{config.server_port}"
    process = await create_subprocess_exec(
        executable,
        "-c",
        "from server import main; main()",
        env=environ.copy(),
    )

    try:
        while True:
            try:
                get(f"{url}/api/health", timeout=None)  # noqa: ASYNC210, S113
                break

            except ConnectError:
                await sleep(1)

        yield url

    finally:
        process.kill()
        await process.wait()


@fixture(scope="session")
def subprocess_client(app_url: str) -> TranslatorClient:
    return TranslatorClient(base_url=app_url)


@fixture(scope="session")
def subprocess_async_client(app_url: str) -> AsyncTranslatorClient:
    return AsyncTranslatorClient(base_url=app_url)


@fixture
def subprocess_client_with_auth(app_url: str) -> TranslatorClient:
    return TranslatorClient(base_url=app_url, auth_token="testtoken")  # noqa: S106


@fixture
def subprocess_async_client_with_auth(app_url: str) -> AsyncTranslatorClient:
    return AsyncTranslatorClient(base_url=app_url, auth_token="testtoken")  # noqa: S106
