from typing import Annotated, get_args

from litestar import Controller, get, post
from litestar.openapi.spec.example import Example
from litestar.params import Parameter
from litestar.response.sse import ServerSentEvent
from litestar.status_codes import HTTP_200_OK

from server.schemas.v1 import Translated, Translation
from server.typedefs import AppState, Language


class TranslatorController(Controller):
    """
    Summary
    -------
    the `/translator` controller handles translations of an input from a source language to a target
    """

    path = '/translator'

    @get(cache=True, sync_to_thread=True)
    def translator_get(
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
            Language,
            Parameter(
                description='source language in the FLORES-200 code format',
                examples=[Example(summary=code, value=code) for code in get_args(Language.__value__)],
            ),
        ] = 'eng_Latn',
        target: Annotated[
            Language,
            Parameter(
                description='target language in the FLORES-200 code format',
                examples=[Example(summary=code, value=code) for code in get_args(Language.__value__)],
            ),
        ] = 'spa_Latn',
    ) -> Translated:
        """
        Summary
        -------
        the GET variant of the `/translator` route
        """
        return Translated(result=state.translator.translate(text, source, target))

    @post(status_code=HTTP_200_OK, sync_to_thread=True)
    def translator_post(self, state: AppState, data: Translation) -> Translated:
        """
        Summary
        -------
        the POST variant of the `/translator` route
        """
        return Translated(result=state.translator.translate(data.text, data.source, data.target))

    @get('/stream', sync_to_thread=True)
    def translator_stream(
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
            Language,
            Parameter(
                description='source language in the FLORES-200 code format',
                examples=[Example(summary=code, value=code) for code in get_args(Language.__value__)],
            ),
        ] = 'eng_Latn',
        target: Annotated[
            Language,
            Parameter(
                description='target language in the FLORES-200 code format',
                examples=[Example(summary=code, value=code) for code in get_args(Language.__value__)],
            ),
        ] = 'spa_Latn',
        event_type: Annotated[
            str | None, Parameter(description='the event that an event listener will listen for')
        ] = None,
    ) -> ServerSentEvent:
        """
        Summary
        -------
        the `/translator/stream` returns a Server-Sent Event stream of the translation
        """
        return ServerSentEvent(state.translator.translate_stream(text, source, target), event_type=event_type)
