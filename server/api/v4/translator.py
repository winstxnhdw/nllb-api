from typing import Annotated, get_args

from litestar import Controller, Response, delete, get, post, put
from litestar.openapi.spec.example import Example
from litestar.params import Parameter
from litestar.response.sse import ServerSentEvent
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_304_NOT_MODIFIED

from server.guards import requires_secret
from server.schemas.v1 import Translated, Translation
from server.typedefs import AppState, Language


class TranslatorController(Controller):
    """
    Summary
    -------
    the `/translator` controller handles translations of an input from a source language to a target
    """

    path = '/translator'

    @delete(guards=[requires_secret], sync_to_thread=True)
    def unload_model(
        self,
        state: AppState,
        *,
        to_cpu: Annotated[bool, Parameter(description='whether to unload the model to CPU')] = False,
    ) -> Response[None]:
        """
        Summary
        -------
        unload the model from the current device
        """
        return Response(
            content=None,
            status_code=HTTP_204_NO_CONTENT if state.translator.unload_model(to_cpu=to_cpu) else HTTP_304_NOT_MODIFIED,
        )

    @put(guards=[requires_secret], sync_to_thread=True)
    def load_model(
        self,
        state: AppState,
        *,
        keep_cache: Annotated[bool, Parameter(description='whether to keep the model cache in RAM')] = False,
    ) -> Response[None]:
        """
        Summary
        -------
        load the model back to the initial device
        """
        return Response(
            content=None,
            status_code=HTTP_204_NO_CONTENT
            if state.translator.load_model(keep_cache=keep_cache)
            else HTTP_304_NOT_MODIFIED,
        )

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
