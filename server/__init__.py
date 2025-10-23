from granian.constants import Interfaces
from granian.server import Server

from server.app import app
from server.config import Config


def main() -> None:
    """
    Summary
    -------
    programmatically run the server with Granian
    """
    config = Config()
    granian = Server(
        f"{app.__module__}:{app.__name__}",
        address="0.0.0.0",
        port=config.server_port,
        interface=Interfaces.ASGI,
        workers=config.worker_count,
        log_access=True,
        log_access_format='[%(time)s] %(status)d "%(method)s %(path)s %(protocol)s" %(addr)s in %(dt_ms).2f ms',
        url_path_prefix=config.server_root_path,
        factory=True,
        reload=False,
    )

    granian.serve()


if __name__ == "__main__":
    main()
