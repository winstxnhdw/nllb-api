from typing import Literal

from litestar import get


@get('/', sync_to_thread=False)
def index() -> Literal['Welcome to v4 of the API!']:
    """
    Summary
    -------
    the `/` route
    """
    return 'Welcome to v4 of the API!'
