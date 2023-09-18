from hypercorn.run import run

from server.config import Config


def main():
    """
    Summary
    -------
    exhaust the initialise generator and run the server
    """
    run(Config())

if __name__ == '__main__':
    main()
