from typing import Literal

from server.api.v1 import v1


@v1.get('/', response_model=Literal['Welcome to v1 of the API!'])
async def index():
    """
    Summary
    -------
    the `/` route
    """
    return 'Welcome to v1 of the API!'
