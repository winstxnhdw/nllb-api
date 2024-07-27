from contextlib import asynccontextmanager
from typing import AsyncIterator

from server.features import TranslatorPool


@asynccontextmanager
async def load_nllb_model(_) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the NLLB model
    """
    TranslatorPool.load()
    yield
