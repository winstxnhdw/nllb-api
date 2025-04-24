from typing import Literal

from litestar.config.cors import CORSConfig
from litestar.types import Method

from server.config import Config


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


def cors() -> CORSConfig:
    """
    Summary
    -------
    get the CORS config

    Returns
    -------
    cors_config (CORSConfig)
        the CORS config
    """
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

    return CORSConfig(
        allow_origins=extract_cors_values(Config.access_control_allow_origin),
        allow_methods=[method for method, is_allowed in allow_methods_dict.items() if is_allowed],
        allow_credentials=Config.access_control_allow_credentials,
        allow_headers=extract_cors_values(Config.access_control_allow_headers),
        expose_headers=extract_cors_values(Config.access_control_expose_headers),
        max_age=Config.access_control_max_age,
    )
