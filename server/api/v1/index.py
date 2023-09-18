from fastapi.responses import PlainTextResponse

from server.api.v1 import v1


@v1.get('/', response_class=PlainTextResponse)
def index():
    """
    Summary
    -------
    the `/` route
    """
    return 'Welcome to v1 of the API!'
