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

    @get(cache=True, sync_to_thread=True, deprecated=True)
    def translate_get(
        self,
        state: AppState,
        text: Annotated[
            str,
            Parameter(
                min_length=1,
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
                description='target language in the FLORES-200 code format',
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
        return Translated(result=state.translator.translate(text, source, target))

    @post(status_code=HTTP_200_OK, sync_to_thread=True, deprecated=True)
    def translate_post(self, state: AppState, data: Translation) -> Translated:
        """
        Summary
        -------
        the POST variant of the `/translate` route
        """
        return Translated(result=state.translator.translate(data.text, data.source, data.target))
