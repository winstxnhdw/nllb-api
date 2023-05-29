
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from server.api.v1 import v1
from server.features.translator import Translator
from server.schemas.v1 import Translation


@v1.post('/translate', response_model=str)
async def translate(request: Translation):
    """
    Summary
    -------
    the `/translate` route
    """
    if not (result := Translator.translate(request.text, request.source, request.target)):
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Translation failed!')

    return result
