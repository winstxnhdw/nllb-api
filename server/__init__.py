from litestar import Litestar, Response
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from server.api import v2, v3
from server.config import Config
from server.lifespans import load_fasttext_model, load_nllb_model
from server.middlewares import LoggingMiddleware


def exception_handler(_, exception: Exception):
    """
    Summary
    -------
    the Litestar exception handler

    Parameters
    ----------
    request (Request) : the request
    exception (Exception) : the exception
    """
    LoggingMiddleware.logger.error('Application Exception', exc_info=exception)

    return Response(
        content={'detail': 'Internal Server Error'},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def initialise() -> Litestar:
    """
    Summary
    -------
    initialises everything

    Returns
    ------
    app (Framework) : an extended FastAPI instance
    """
    openapi_config = OpenAPIConfig(
        title='nllb-api',
        version='3.0.0',
        servers=[Server(url=Config.server_root_path)],
    )

    return Litestar(
        openapi_config=openapi_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exception_handler},
        middleware=[LoggingMiddleware],
        route_handlers=[v2, v3],
        lifespan=[load_fasttext_model, load_nllb_model],
    )
