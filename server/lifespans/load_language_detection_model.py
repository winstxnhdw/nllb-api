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
    """
    config = state.config

    with get_language_detector(
        config.language_detector_repository,
        stub=config.stub_language_detector,
    ) as language_detector:
        state.language_detector = language_detector
        yield
