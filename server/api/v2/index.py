from typing import Literal

from starlette.responses import PlainTextResponse

from server.api.v2 import v2


@v2.get('/', response_model=Literal['Welcome to v2 of the API!'])
def index():
    """
    Summary
    -------
    the `/` route
    """
    return PlainTextResponse('Welcome to v2 of the API!')
