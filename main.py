from hypercorn.run import run

from server.config import Config


def main():
    """
    Summary
    -------
    programmatically run the server with Hypercorn
    """
    run(Config())

if __name__ == '__main__':
    main()
