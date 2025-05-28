from logging import getLogger
from typing import Literal

from litestar import Litestar, Response, Router
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.types import Method

from server.api import v4
from server.config import Config
from server.lifespans import load_fasttext_model, load_translator_model


def exception_handler(_, exception: Exception) -> Response[dict[str, str]]:
    """
    Summary
    -------
    the Litestar exception handler

    Parameters
    ----------
    request (Request) : the request
    exception (Exception) : the exception

    Returns
    -------
    response (Response[dict[str, str]]) : the response
    """
    getLogger('custom.access').error(exception, exc_info=True)

    return Response(
        content={'detail': 'Internal Server Error'},
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


def app() -> Litestar:
    """
    Summary
    -------
    the Litestar application
    """
    description = (
        "A performant high-throughput CPU-based API for Meta's No Language Left Behind (NLLB) using CTranslate2, "
        'hosted on Hugging Face Spaces.'
    )

    openapi_config = OpenAPIConfig(
        title=Config.app_name,
        version='4.2.0',
        description=description,
        use_handler_docstrings=True,
        servers=[Server(url=Config.server_root_path)],
    )

    v4_router = Router(
        '/v4',
        tags=['v4'],
        route_handlers=[v4.language, v4.TranslatorController],
    )

    allow_methods_dict: dict[Method | Literal['*'], bool] = {
        'GET': Config.access_control_allow_method_get,
        'POST': Config.access_control_allow_method_post,
        'PUT': Config.access_control_allow_method_put,
        'DELETE': Config.access_control_allow_method_delete,
        'OPTIONS': Config.access_control_allow_method_options,
        'PATCH': Config.access_control_allow_method_patch,
        'HEAD': Config.access_control_allow_method_head,
        'TRACE': Config.access_control_allow_method_trace,
    }

    cors_config = CORSConfig(
        allow_origins=extract_cors_values(Config.access_control_allow_origin),
        allow_methods=[method for method, is_allowed in allow_methods_dict.items() if is_allowed],
        allow_credentials=Config.access_control_allow_credentials,
        allow_headers=extract_cors_values(Config.access_control_allow_headers),
        expose_headers=extract_cors_values(Config.access_control_expose_headers),
        max_age=Config.access_control_max_age,
    )

    return Litestar(
        openapi_config=openapi_config,
        cors_config=cors_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exception_handler},
        route_handlers=[PrometheusController, v4_router],
        lifespan=[load_fasttext_model, load_translator_model],
        middleware=[PrometheusConfig(app_name=Config.app_name).middleware],
    )
