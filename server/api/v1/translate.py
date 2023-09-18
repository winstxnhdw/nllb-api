from typing import Annotated, Generator

from fastapi import Depends

from server.api.v1 import v1
from server.dependencies import translation
from server.schemas.v1 import Translated


@v1.post('/translate', response_model=Translated)
def translate(result: Annotated[Generator[str, None, None], Depends(translation)]):
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    return Translated(text=''.join(result))
