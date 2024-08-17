# pylint: disable=missing-function-docstring,redefined-outer-name

from typing import AsyncIterator, Literal

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from server import App


@fixture
def anyio_backend() -> tuple[Literal['asyncio', 'trio'], dict[str, bool]]:
    return 'asyncio', {'use_uvloop': True}


@fixture(scope='function')
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=App.asgi) as client:
        yield client
