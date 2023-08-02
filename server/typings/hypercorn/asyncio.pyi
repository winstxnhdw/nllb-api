# pylint: skip-file

from typing import Awaitable, Callable, Literal

from fastapi import FastAPI
from hypercorn import Config

async def serve(
    app: FastAPI,
    config: Config,
    shutdown_trigger: Callable[..., Awaitable[None]] | None = None,
    mode: Literal['asgi', 'wsgi'] | None = None
) -> None: ...
