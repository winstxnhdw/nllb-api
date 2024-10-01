from typing import Literal

from litestar import get


@get('/', sync_to_thread=False, deprecated=True)
def index() -> Literal['Welcome to v3 of the API!']:
    """
    Summary
    -------
    the `/` route
    """
    return 'Welcome to v3 of the API!'
