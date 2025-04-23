from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from litestar import Litestar

from server.features import get_language_detector


@asynccontextmanager
async def load_fasttext_model(app: Litestar) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the FastText model

    Parameters
    ----------
    app (Litestar)
        the application instance
    """
    app.state.language_detector = get_language_detector()

    try:
        yield

    finally:
        del app.state.language_detector
