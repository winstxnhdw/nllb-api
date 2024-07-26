from uvicorn import run

from server import initialise
from server.config import Config


def main():
    """
    Summary
    -------
    programmatically run the server with Uvicorn
    """
    run(
        f'{initialise.__module__}:{initialise.__name__}',
        host='0.0.0.0',
        port=Config.server_port,
        reload=False,
        loop='uvloop',
        http='httptools',
        use_colors=True,
        factory=True,
    )


if __name__ == '__main__':
    main()
