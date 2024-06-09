from asyncio import gather
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from server.lifespans.load_fasttext_model import load_fasttext_model
from server.lifespans.load_nllb_model import load_nllb_model


@asynccontextmanager
async def lifespans(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    Summary
    -------
    the FastAPI lifespan function
    """
    await gather(load_nllb_model(), load_fasttext_model())
    yield
