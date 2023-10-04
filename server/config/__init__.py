from hypercorn import Config as HypercornConfig

from server.config.exceptions import (InvalidPortError, InvalidRootPathError,
                                      InvalidWorkerCountError)
from server.config.get_config import get_config


class Config(HypercornConfig):
    """
    Summary
    -------
    the config class for the server

    Attributes
    ----------
    server_root_path (str) : the root path of the server
    worker_count (int) : the number of workers to use
    """
    server_root_path = get_config('ROOT_PATH', str, InvalidRootPathError, '/api')
    worker_count = get_config('WORKER_COUNT', int, InvalidWorkerCountError, 2)

    def __init__(self, default_port: int = 49494):

        if (port := get_config('SERVER_PORT', int, InvalidPortError, default_port)) == default_port:
            print(f'WARNING: using default port {default_port}')

        self.application_path = 'server:initialise()'
        self.bind = [f"0.0.0.0:{port}"]
        self.access_log_format = '%(s)s "%(R)s" %(h)s "%(a)s"'
        self.accesslog = '-'
        self.use_reloader = False
        self.startup_timeout = 300
        self.worker_class = 'uvloop'
        self.workers = self.worker_count

        super().__init__()
