from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from litestar import Litestar

from server.typedefs import AppState


def inject_state(
    lifespan: Callable[[Litestar, AppState], AbstractAsyncContextManager[None]],
) -> Callable[[Litestar], AbstractAsyncContextManager[None]]:
    return lambda app: lifespan(
        app,
        app.state,  # pyright: ignore [reportArgumentType]
    )
