from collections.abc import AsyncIterator
from enum import IntEnum
from typing import Literal

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from server import app


class StatusCode(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500


@fixture
def anyio_backend() -> tuple[Literal['asyncio', 'trio'], dict[str, bool]]:
    return 'asyncio', {'use_uvloop': True}


@fixture
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app()) as client:
        yield client
