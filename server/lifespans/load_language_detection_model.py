from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from server.features import get_language_detector
from server.lifespans.inject_state import inject_state
from server.typedefs import AppState


@inject_state
@asynccontextmanager
async def load_fasttext_model(_, state: AppState) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the FastText model

    Parameters
    ----------
    app (Litestar)
        the application instance

    state (AppState)
        the application state
    """
    config = state.config

    state.language_detector = get_language_detector(
        config.language_detector_repository,
        stub=config.stub_language_detector,
    )

    try:
        yield

    finally:
        del state.language_detector
