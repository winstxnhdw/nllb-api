from os import environ as env

from hypercorn import Config as HypercornConfig

from server.config.exceptions import NoPortFoundError


class Config(HypercornConfig):
    """
    Summary
    -------
    the config class for the server
    """
    default_port = 49494

    if not (SERVER_PORT := env.get('SERVER_PORT', default_port)):
        if not isinstance(SERVER_PORT, int):
            raise NoPortFoundError

    if SERVER_PORT == default_port:
        print(f'WARNING: using default port {default_port}')

    _bind = [f"0.0.0.0:{SERVER_PORT}"]
    access_log_format = '%(s)s "%(R)s" %(h)s "%(a)s"'
    accesslog = '-'
