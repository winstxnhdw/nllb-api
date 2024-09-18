from asyncio import wrap_future
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, get_args

from litestar import Controller, get, post
from litestar.openapi.spec.example import Example
from litestar.params import Parameter
from litestar.status_codes import HTTP_200_OK

from server.schemas.v1 import Translated, Translation
from server.state import AppState
from server.types import Languages


class TranslateController(Controller):
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target
    """

    path = '/translate'
    thread_pool = ThreadPoolExecutor()

    @get(cache=True)
    async def translate_get(
        self,
        state: AppState,
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
                examples=[Example(summary=code, value=code) for code in get_args(Languages.__value__)],  # pylint: disable=no-member
            ),
        ],
        target: Annotated[
            Languages,
            Parameter(
                description='source language in the FLORES-200 code format',
                default='spa_Latn',
                examples=[Example(summary=code, value=code) for code in get_args(Languages.__value__)],  # pylint: disable=no-member
            ),
        ],
    ) -> Translated:
        """
        Summary
        -------
        the GET variant of the `/translate` route
        """
        translate_job = self.thread_pool.submit(state.translator.translate, text, source, target)
        return Translated(result=await wrap_future(translate_job))

    @post(status_code=HTTP_200_OK)
    async def translate_post(self, state: AppState, data: Translation) -> Translated:
        """
        Summary
        -------
        the POST variant of the `/translate` route
        """
        translate_job = self.thread_pool.submit(state.translator.translate, data.text, data.source, data.target)
        return Translated(result=await wrap_future(translate_job))
