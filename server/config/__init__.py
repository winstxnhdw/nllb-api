from os import environ as env

from hypercorn import Config as HypercornConfig

from server.config.exceptions import NoPortFoundError


class Config(HypercornConfig):
    """
    Summary
    -------
    the config class for the server
    """
    if not (SERVER_PORT := env['SERVER_PORT']):
        raise NoPortFoundError

    _bind = [f"0.0.0.0:{SERVER_PORT}"]
    access_log_format = '%(s)s "%(R)s" %(h)s "%(a)s"'
    accesslog = '-'
