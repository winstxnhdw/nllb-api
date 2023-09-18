from fastapi.responses import PlainTextResponse

from server.api.v2 import v2


@v2.get('/', response_class=PlainTextResponse)
def index():
    """
    Summary
    -------
    the `/` route
    """
    return 'Welcome to v2 of the API!'
