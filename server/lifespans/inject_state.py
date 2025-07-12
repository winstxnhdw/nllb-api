from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from litestar import Litestar

from server.typedefs import AppState


def inject_state(
    lifespan: Callable[[Litestar, AppState], AbstractAsyncContextManager[None]],
) -> Callable[[Litestar], AbstractAsyncContextManager[None]]:
    """
    Summary
    -------
    decorator to inject the application state into the lifespan context manager

    Parameters
    ----------
    lifespan (Callable[[Litestar, AppState], AbstractAsyncContextManager[None]])
        the lifespan context manager that will receive the application state

    Returns
    -------
    lifespan (Callable[[Litestar], AbstractAsyncContextManager[None]])
        a Litestar-compatible lifespan context manager
    """
    return lambda app: lifespan(
        app,
        app.state,  # pyright: ignore [reportArgumentType]
    )
