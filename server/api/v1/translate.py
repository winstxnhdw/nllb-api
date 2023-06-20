from typing import Literal

from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from server.api.v1 import v1
from server.features.translator import Translator
from server.schemas.v1 import Translation


@v1.post('/translate', response_model=Literal['¡Hola, mundo!'])
async def translate(request: Translation):
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    try:
        result = Translator.translate(request.text, request.source, request.target)

    except KeyError as exception:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Invalid source or target language!') from exception

    if not result:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Translation failed!')

    return result
