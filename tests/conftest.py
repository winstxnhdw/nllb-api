from collections.abc import AsyncIterator
from typing import Literal

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from server.app import app


@fixture
def anyio_backend() -> tuple[Literal['asyncio', 'trio'], dict[str, bool]]:
    return 'asyncio', {'use_uvloop': True}


@fixture
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app(), backend_options={'use_uvloop': True}) as client:
        yield client
