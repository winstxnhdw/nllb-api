from server.initialise_routes import initialise_routes
from server.initialise_server import initialise_server


def initialise():
    """
    Summary
    -------
    initialises everything
    """
    initialise_routes()
    initialise_server()
