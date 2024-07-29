from granian import Granian
from granian.constants import Interfaces

from server import App
from server.config import Config


def main():
    """
    Summary
    -------
    programmatically run the server with Granian
    """
    granian = Granian(
        f'{App.__module__}:{App.__name__}',
        '0.0.0.0',
        Config.server_port,
        Interfaces.ASGI,
        Config.worker_count,
        loop_opt=True,
        log_access=True,
        log_access_format='[%(time)s] %(status)d "%(method)s %(path)s %(protocol)s" %(addr)s in %(dt_ms).2f ms',
        url_path_prefix=Config.server_root_path,
        reload=False,
    )

    granian.serve()


if __name__ == '__main__':
    main()
