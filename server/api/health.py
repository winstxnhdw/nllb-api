from litestar import get
from litestar.status_codes import HTTP_204_NO_CONTENT


@get('/health', sync_to_thread=False, status_code=HTTP_204_NO_CONTENT)
def health() -> None:
    """
    Summary
    -------
    the `/health` endpoint will only return a 204 status code
    """
    return
