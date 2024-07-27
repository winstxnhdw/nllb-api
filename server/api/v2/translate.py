from asyncio import gather

from litestar import Controller, post

from server.features import TranslatorPool
from server.schemas.v1 import Translation


class TranslateController(Controller):
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """

    path = '/translate'

    @post(deprecated=True)
    async def translate(self, data: Translation) -> str:
        """
        Summary
        -------
        a deprecated version of the `/translate` route
        """
        results = await gather(
            *(TranslatorPool.translate(line, data.source, data.target) for line in data.text.splitlines() if line)
        )

        return '\n'.join(results)
