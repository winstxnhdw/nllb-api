from logging import INFO, WARN, StreamHandler, getLogger
from time import process_time, strftime
from typing import Awaitable, Callable

from starlette.types import ASGIApp, Message, Receive, Scope, Send


class LoggingMiddleware:
    """
    Summary
    -------
    a middleware to log requests

    Attributes
    ----------
    logger (Logger) : a custom logger
    app (ASGIApp) : the ASGI application
    """

    def __init__(self, app: ASGIApp):
        getLogger('uvicorn.access').setLevel(WARN)
        self.logger = getLogger('custom.access')
        self.logger.setLevel(INFO)
        self.logger.addHandler(StreamHandler())
        self.app = app

    async def inner_send(self, message: Message, send: Send, status_code: list[int]):
        """
        Summary
        -------
        a function to log the requests

        Parameters
        ----------
        message (Message) : the message
        send (Send) : the send function
        status_code (list[int]) : the status code
        """
        if message['type'] == 'http.response.start':
            status_code[0] = message['status']

        await send(message)

    def inner_send_factory(self, send: Send, status_code: list[int]) -> Callable[[Message], Awaitable[None]]:
        """
        Summary
        -------
        a factory to create the inner send function

        Parameters
        ----------
        send (Send) : the send function
        status_code (list[int]) : the status code

        Returns
        -------
        inner_send (Callable[[Message], Awaitable[None]]) : a custom send function
        """
        return lambda message: self.inner_send(message, send, status_code)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        start_process_time = process_time()
        status_code = [500]
        user_agents = [v for k, v in scope['headers'] if k.lower() == b'user-agent']
        user_agent = 'NIL' if not user_agents else user_agents[0].decode()
        client = scope['client']
        client_ip = 'NIL' if not client else client[0]

        try:
            await self.app(scope, receive, self.inner_send_factory(send, status_code))

        finally:
            self.logger.info(
                '[%s] [INFO] %d "%s %s" %s "%s" in %.4f ms',
                strftime('%Y-%m-%d %H:%M:%S %z'),
                status_code[0],
                scope['method'],
                scope['path'],
                client_ip,
                user_agent,
                (process_time() - start_process_time) * 1000,
            )
