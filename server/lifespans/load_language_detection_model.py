from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from litestar import Litestar

from server.features.detector import get_language_detector


@asynccontextmanager
async def language_detector_lifespan(
    app: Litestar,
    *,
    stub: bool,
) -> AsyncGenerator[None]:
    """
    Summary
    -------
    lifespan to load the language detection model

    Parameters
    ----------
    app (Litestar)
        the application instance

    stub (bool)
        whether to use a stub object
    """
    app.state.language_detector = get_language_detector(stub=stub)

    try:
        yield

    finally:
        del app.state.language_detector


def load_language_detector(
    *,
    stub: bool,
) -> Callable[[Litestar], AbstractAsyncContextManager[None]]:
    """
    Summary
    -------
    the language detector lifespan factory

    Parameters
    ----------
    stub (bool)
        whether to use a stub object

    Returns
    -------
    lifespan (Callable[[Litestar], AbstractAsyncContextManager[None]])
        a Litestar-compatible lifespan context manager
    """
    return lambda app: language_detector_lifespan(
        app,
        stub=stub,
    )
