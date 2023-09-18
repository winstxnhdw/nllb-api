from typing import Generator

from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from server.features import Translator
from server.schemas.v1 import Translation


def translation(request: Translation) -> Generator[str, None, None]:
    """
    Summary
    -------
    translate the input from the source language to the target language

    Parameters
    ----------
    input (str) : the input to translate
    source_language (str) : the source language
    target_language (str) : the target language

    Returns
    -------
    translated_text (str) : the translated text
    """
    try:
        result = Translator.translate(request.text, request.source, request.target)

    except KeyError as exception:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Invalid source or target language!') from exception

    if not result:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Translation failed!')

    return result
