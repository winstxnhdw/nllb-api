from typing import Annotated

from litestar import Controller, get, post
from litestar.openapi.spec.example import Example
from litestar.params import Parameter

from server.features import TranslatorPool
from server.features.types import Languages
from server.schemas.v1 import Translated, Translation


class TranslateController(Controller):
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target
    """

    path = '/translate'

    @get()
    async def translate_get(
        self,
        text: Annotated[str, Parameter(examples=[Example(value='Hello, world!')])],
        source: Annotated[Languages, Parameter(examples=[Example(value='eng_Latn')])],
        target: Annotated[Languages, Parameter(examples=[Example(value='spa_Latn')])],
    ) -> Translated:
        """
        Summary
        -------
        the GET variant of the `/translate` route
        """
        return Translated(result=await TranslatorPool.translate(text, source, target))

    @post()
    async def translate_post(self, data: Translation) -> Translated:
        """
        Summary
        -------
        the POST variant of the `/translate` route
        """
        return Translated(result=await TranslatorPool.translate(data.text, data.source, data.target))
