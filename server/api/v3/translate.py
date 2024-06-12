from typing import Annotated

from fastapi import Query

from server.api.v3 import v3
from server.features import Translator
from server.features.types import Languages
from server.schemas.v1 import Translated, Translation


@v3.get('/translate')
async def translate_get(
    text: Annotated[str, Query(examples=['Hello, world!'])],
    source: Annotated[Languages, Query(examples=['eng_Latn'])],
    target: Annotated[Languages, Query(examples=['spa_Latn'])],
) -> Translated:
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    return Translated(result=await Translator.translate(text, source, target))


@v3.post('/translate')
async def translate_post(request: Translation) -> Translated:
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    return Translated(result=await Translator.translate(request.text, request.source, request.target))
