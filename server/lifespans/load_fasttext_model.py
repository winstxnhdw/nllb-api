from contextlib import asynccontextmanager
from typing import AsyncIterator

from server.features import LanguageDetector


@asynccontextmanager
async def load_fasttext_model(_) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the FastText model
    """
    LanguageDetector.load()
    yield
