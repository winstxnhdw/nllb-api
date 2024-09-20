from contextlib import asynccontextmanager
from typing import AsyncIterator

from litestar import Litestar

from server.features import get_translator


@asynccontextmanager
async def load_translator_model(app: Litestar) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the NLLB model

    Parameters
    ----------
    app (Litestar) : the application instance
    """
    app.state.translator = get_translator()

    try:
        yield
    finally:
        del app.state.translator.translator
