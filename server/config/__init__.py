from os import environ as env

from hypercorn import Config as HypercornConfig

from server.config.exceptions import NoPortFoundError


class Config(HypercornConfig):
    """
    Summary
    -------
    the config class for the server
    """
    def __init__(self, default_port: int = 49494):

        if not (port := env.get('SERVER_PORT', default_port)):
            if not isinstance(port, int):
                raise NoPortFoundError

        if port == default_port:
            print(f'WARNING: using default port {default_port}')

        self.application_path = 'server:initialise()'
        self.bind = [f"0.0.0.0:{port}"]
        self.access_log_format = '%(s)s "%(R)s" %(h)s "%(a)s"'
        self.accesslog = '-'
        self.use_reloader = True
        self.worker_class = 'uvloop'
        self.workers = 2

        super().__init__()
