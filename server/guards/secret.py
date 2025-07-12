from typing import Any

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def requires_secret(connection: ASGIConnection[Any, Any, Any, Any], route_handler: BaseRouteHandler) -> None:
    """
    Summary
    -------
    guards the route with a secret token

    Parameters
    ----------
    connection (ASGIConnection[Any, Any, Any, Any])
        the ASGI connection

    route_handler (BaseRouteHandler)
        the route handler
    """
    if connection.headers.get('Authorization', '') != route_handler.opt.get('auth_token'):
        raise NotAuthorizedException
