from typing import Annotated

from fastapi import Query

from server.api.v3 import v3
from server.features import LanguageDetector
from server.schemas.v1 import Language


@v3.get('/detect_language')
async def detect_language(text: Annotated[str, Query(max_length=20, example='Hello, world!')]) -> Language:
    """
    Summary
    -------
    the `/detect_language` route detects the language of the input text
    """
    return Language(language=await LanguageDetector.detect(text))
