from granian import Granian
from granian.constants import Interfaces

from server import app
from server.config import Config


def main():
    """
    Summary
    -------
    programmatically run the server with Granian
    """
    granian = Granian(
        f'{app.__module__}:{app.__name__}',
        '0.0.0.0',
        Config.server_port,
        Interfaces.ASGI,
        Config.worker_count,
        log_access=True,
        log_access_format='[%(time)s] %(status)d "%(method)s %(path)s %(protocol)s" %(addr)s in %(dt_ms).2f ms',
        url_path_prefix=Config.server_root_path,
        factory=True,
        reload=False,
    )

    granian.serve()


if __name__ == '__main__':
    main()
