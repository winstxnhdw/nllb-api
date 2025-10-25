from collections.abc import AsyncIterator, Callable
from typing import Literal

from litestar import Litestar
from litestar.testing import AsyncTestClient
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


@fixture(scope="session")
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
