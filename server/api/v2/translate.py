from fastapi.responses import StreamingResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from server.api.v2 import v2
from server.features import Translator
from server.schemas.v1 import Translation


@v2.post('/translate')
def translate(request: Translation):
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

    return StreamingResponse(result, media_type='text/plain')
