from functools import partial
from logging import Logger, getLogger
from typing import Literal

from litestar import Litestar, Response, Router
from litestar.config.cors import CORSConfig
from litestar.datastructures import State
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.types import Method

from server.api import health, v4
from server.config import Config
from server.lifespans import consul_register, load_fasttext_model, load_translator_model


def exception_handler(logger: Logger, _, exception: Exception) -> Response[dict[str, str]]:
    """
    Summary
    -------
    the Litestar exception handler

    Parameters
    ----------
    logger (Logger)
        the logger instance

    request (Request)
        the request

    exception (Exception)
        the exception

    Returns
    -------
    response (Response[dict[str, str]]) : the response
    """
    error_message = 'Internal Server Error'
    logger.error(error_message, exc_info=exception)

    return Response(
        content={'detail': error_message},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def extract_cors_values(string: str) -> list[str]:
    """
    Summary
    -------
    split a string by commas

    Parameters
    ----------
    string (str)
        the string to split

    Returns
    -------
    strings (list[str])
        the list of strings
    """
    return [stripped_chunk for chunk in string.split(',') if (stripped_chunk := chunk.strip())]


def app(config: Config | None = None) -> Litestar:
    """
    Summary
    -------
    the Litestar application
    """
    config = config or Config()
    app_name = config.app_name
    logger = getLogger(app_name)
    description = (
        "A performant high-throughput CPU-based API for Meta's No Language Left Behind (NLLB) using CTranslate2, "
        'hosted on Hugging Face Spaces.'
    )

    openapi_config = OpenAPIConfig(
        title=app_name,
        version='4.2.0',
        description=description,
        use_handler_docstrings=True,
        servers=[Server(url=config.server_root_path)],
    )

    v4_router = Router(
        '/v4',
        tags=['v4'],
        route_handlers=[v4.language, v4.TranslatorController],
    )

    allow_methods_dict: dict[Method | Literal['*'], bool] = {
        'GET': config.access_control_allow_method_get,
        'POST': config.access_control_allow_method_post,
        'PUT': config.access_control_allow_method_put,
        'DELETE': config.access_control_allow_method_delete,
        'OPTIONS': config.access_control_allow_method_options,
        'PATCH': config.access_control_allow_method_patch,
        'HEAD': config.access_control_allow_method_head,
        'TRACE': config.access_control_allow_method_trace,
    }

    cors_config = CORSConfig(
        allow_origins=extract_cors_values(config.access_control_allow_origin),
        allow_methods=[method for method, is_allowed in allow_methods_dict.items() if is_allowed],
        allow_credentials=config.access_control_allow_credentials,
        allow_headers=extract_cors_values(config.access_control_allow_headers),
        expose_headers=extract_cors_values(config.access_control_expose_headers),
        max_age=config.access_control_max_age,
    )

    return Litestar(
        openapi_config=openapi_config,
        cors_config=cors_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: partial(exception_handler, logger)},
        route_handlers=[PrometheusController, v4_router, health],
        lifespan=[load_fasttext_model, load_translator_model, consul_register],
        middleware=[PrometheusConfig(app_name).middleware],
        state=State({'config': config}),
        opt={'auth_token': config.auth_token},
    )
