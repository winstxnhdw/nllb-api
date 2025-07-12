from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from server.features import get_translator
from server.lifespans.inject_state import inject_state
from server.typedefs import AppState


@inject_state
@asynccontextmanager
async def load_translator_model(_, state: AppState) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the NLLB model

    Parameters
    ----------
    app (Litestar)
        the application instance

    state (AppState)
        the application state
    """
    config = state.config

    with get_translator(
        config.translator_repository,
        translator_threads=config.translator_threads,
        stub=config.stub_translator,
        use_cuda=config.use_cuda,
    ) as translator:
        state.translator = translator
        yield
