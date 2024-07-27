from asyncio import gather

from starlette.responses import PlainTextResponse

from server.api.v2 import v2
from server.features import TranslatorPool
from server.schemas.v1 import Translation


@v2.post('/translate', deprecated=True)
async def translate(request: Translation) -> PlainTextResponse:
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    results = await gather(
        *(TranslatorPool.translate(line, request.source, request.target) for line in request.text.splitlines() if line)
    )

    return PlainTextResponse('\n'.join(results))
