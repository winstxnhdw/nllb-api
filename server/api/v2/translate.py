from typing import Annotated, Generator

from fastapi import Depends
from starlette.responses import StreamingResponse

from server.api.v2 import v2
from server.dependencies import translation


@v2.post('/translate')
def translate(result: Annotated[Generator[str, None, None], Depends(translation)]):
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    return StreamingResponse(result, media_type='text/event-stream')
