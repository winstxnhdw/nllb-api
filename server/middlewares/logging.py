from logging import INFO, WARN, StreamHandler, getLogger
from time import process_time, strftime

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Summary
    -------
    a middleware to log the requests

    Attributes
    ----------
    logger (Logger) : a custom logger

    Methods
    -------
    log_request(request: Request, call_next: RequestResponseEndpoint) -> Response
        log the request

    dispatch(request: Request, call_next: RequestResponseEndpoint) -> Response
        dispatch the request
    """
    def __init__(self, app: ASGIApp, dispatch: DispatchFunction | None = None):

        super().__init__(app, dispatch)

        getLogger('uvicorn.access').setLevel(WARN)
        self.logger = getLogger('custom.access')
        self.logger.setLevel(INFO)
        self.logger.addHandler(StreamHandler())


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        start_process_time = process_time()
        response = await call_next(request)

        self.logger.info('[%s] [INFO] %s "%s %s" %s "%s" in %.4f ms',
            strftime('%Y-%m-%d %H:%M:%S %z'),
            response.status_code,
            request.method,
            request.url.path,
            '' if request.client is None else request.client.host,
            request.headers.get('user-agent', ''),
            (process_time() - start_process_time) * 1000
        )

        return response
