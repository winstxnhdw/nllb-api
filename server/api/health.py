from litestar import get

from server.schemas import Health


@get("/health", cache=True, sync_to_thread=False)
def health() -> Health:
    """
    Summary
    -------
    the `/health` route will return a shields.io endpoint badge response
    """
    return Health()
