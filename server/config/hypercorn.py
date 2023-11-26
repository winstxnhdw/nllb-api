from hypercorn import Config as HypercornConfig

from server.config.general import Config


class ServerConfig(HypercornConfig):
    """
    Summary
    -------
    the config class for the server
    """
    def __init__(self, default_port: int = 49494):

        if (port := Config.server_port) == default_port:
            print(f'WARNING: using default port {default_port}')

        self.application_path = 'server:initialise()'
        self.bind = [f"0.0.0.0:{port}"]
        self.access_log_format = '%(s)s "%(R)s" %(h)s "%(a)s"'
        self.accesslog = '-'
        self.use_reloader = False
        self.startup_timeout = 300
        self.worker_class = 'uvloop'
        self.workers = Config.worker_count

        super().__init__()
