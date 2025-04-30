from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from litestar import Litestar

from server.config import Config
from server.features import get_translator


@asynccontextmanager
async def load_translator_model(app: Litestar) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the NLLB model

    Parameters
    ----------
    app (Litestar)
        the application instance
    """
    app.state.translator = get_translator(
        Config.translator_repository,
        translator_threads=Config.translator_threads,
        stub=Config.stub_translator,
        use_cuda=Config.use_cuda,
    )

    try:
        yield

    finally:
        del app.state.translator
