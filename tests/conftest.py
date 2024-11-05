# pylint: disable=missing-function-docstring,redefined-outer-name

from typing import AsyncIterator, Literal

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from server import app


@fixture()
def anyio_backend() -> tuple[Literal['asyncio', 'trio'], dict[str, bool]]:
    return 'asyncio', {'use_uvloop': True}


@fixture()
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app()) as client:
        yield client
