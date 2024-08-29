from logging import getLogger

from litestar import Litestar, Response
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.types import LifeSpanReceive, LifeSpanScope, LifeSpanSend, Receive, Scope, Send

from server.api import v3
from server.config import Config
from server.lifespans import load_fasttext_model, load_nllb_model


def exception_handler(_, exception: Exception) -> Response[dict[str, str]]:
    """
    Summary
    -------
    the Litestar exception handler

    Parameters
    ----------
    request (Request) : the request
    exception (Exception) : the exception
    """
    getLogger('custom.access').error('Application Exception', exc_info=exception)

    return Response(
        content={'detail': 'Internal Server Error'},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


class App:
    """
    Summary
    -------
    the ASGI application wrapper

    Parameters
    ----------
    scope (Scope) : the ASGI scope
    receive (Receive) : the ASGI receive channel
    send (Send) : the ASGI send channel
    """

    description = (
        "A performant high-throughput CPU-based API for Meta's No Language Left Behind (NLLB) using CTranslate2, "
        'hosted on Hugging Face Spaces.'
    )

    openapi_config = OpenAPIConfig(
        title='nllb-api',
        version='3.0.0',
        description=description,
        use_handler_docstrings=True,
        servers=[Server(url=Config.server_root_path)],
    )

    asgi = Litestar(
        openapi_config=openapi_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exception_handler},
        route_handlers=[v3],
        lifespan=[load_fasttext_model, load_nllb_model],
    )

    async def __new__(  # pylint: disable=invalid-overridden-method
        cls,
        scope: Scope | LifeSpanScope,
        receive: Receive | LifeSpanReceive,
        send: Send | LifeSpanSend,
    ):
        await cls.asgi(scope, receive, send)
