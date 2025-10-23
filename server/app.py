from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from functools import partial
from logging import Logger, getLogger
from random import choice
from string import ascii_letters, digits
from typing import Literal

from litestar import Litestar, Response, Router
from litestar.config.cors import CORSConfig
from litestar.contrib.opentelemetry import OpenTelemetryConfig, OpenTelemetryPlugin
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.plugins import PluginProtocol
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.types import Method

from server.api import health, v4
from server.config import Config
from server.lifespans import load_language_detector, load_translator_model
from server.plugins import ConsulPlugin
from server.telemetry import get_log_handler, get_meter_provider, get_tracer_provider


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
    logger.error(exception, exc_info=exception)

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


def app(config: Config | None = None) -> Litestar:
    """
    Summary
    -------
    the Litestar application
    """
    config = config or Config()
    ascii_letters_with_digits = f'{ascii_letters}{digits}'
    app_name = config.app_name
    app_id = f'{app_name}-{"".join(choice(ascii_letters_with_digits) for _ in range(4))}'  # noqa: S311
    logger = getLogger(app_name)
    plugins: list[PluginProtocol] = []
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

    lifespans: tuple[Callable[[Litestar], AbstractAsyncContextManager[None]], ...] = (
        load_language_detector(config.language_detector_repository, stub=config.stub_language_detector),
        load_translator_model(
            config.translator_repository,
            translator_threads=config.translator_threads,
            stub=config.stub_translator,
            use_cuda=config.use_cuda,
        ),
    )

    if config.otel_exporter_otlp_endpoint:
        handler = get_log_handler(otlp_service_name=app_name, otlp_service_instance_id=app_id)
        logger.addHandler(handler)
        getLogger('granian.access').addHandler(handler)
        opentelemetry_config = OpenTelemetryConfig(
            tracer_provider=get_tracer_provider(otlp_service_name=app_name, otlp_service_instance_id=app_id),
            meter_provider=get_meter_provider(otlp_service_name=app_name, otlp_service_instance_id=app_id),
        )

        plugins.append(OpenTelemetryPlugin(opentelemetry_config))

    if config.consul_http_addr and config.consul_service_address:
        consul_plugin = ConsulPlugin(
            app_name=app_name,
            app_id=app_id,
            consul_http_addr=config.consul_http_addr,
            consul_service_address=config.consul_service_address,
            consul_service_port=config.consul_service_port,
            consul_service_scheme=config.consul_service_scheme,
            server_root_path=config.server_root_path,
            consul_auth_token=config.consul_auth_token,
        )

        plugins.append(consul_plugin)

    return Litestar(
        openapi_config=openapi_config,
        cors_config=cors_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: partial(exception_handler, logger)},
        route_handlers=[v4_router, health],
        plugins=plugins,
        lifespan=lifespans,
        opt={'auth_token': config.auth_token},
    )
