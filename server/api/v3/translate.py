from typing import Annotated, get_args

from litestar import Controller, get, post
from litestar.openapi.spec.example import Example
from litestar.params import Parameter
from litestar.status_codes import HTTP_200_OK

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

    @get(cache=True)
    async def translate_get(
        self,
        text: Annotated[
            str,
            Parameter(
                description='source text of a single language',
                examples=[
                    Example(summary='English', value='Hello, world!'),
                    Example(summary='Spanish', value='¡Hola, mundo!'),
                ],
            ),
        ],
        source: Annotated[
            Languages,
            Parameter(
                description='source language in the FLORES-200 code format',
                default='eng_Latn',
                examples=[Example(summary=code, value=code) for code in get_args(Languages.__value__)],
            ),
        ],
        target: Annotated[
            Languages,
            Parameter(
                description='source language in the FLORES-200 code format',
                default='spa_Latn',
                examples=[Example(summary=code, value=code) for code in get_args(Languages.__value__)],
            ),
        ],
    ) -> Translated:
        """
        Summary
        -------
        the GET variant of the `/translate` route
        """
        return Translated(result=await TranslatorPool.translate(text, source, target))

    @post(status_code=HTTP_200_OK)
    async def translate_post(self, data: Translation) -> Translated:
        """
        Summary
        -------
        the POST variant of the `/translate` route
        """
        return Translated(result=await TranslatorPool.translate(data.text, data.source, data.target))
