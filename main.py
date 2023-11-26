from hypercorn.run import run

from server.config.hypercorn import ServerConfig


def main():
    """
    Summary
    -------
    programmatically run the server with Hypercorn
    """
    run(ServerConfig())

if __name__ == '__main__':
    main()
