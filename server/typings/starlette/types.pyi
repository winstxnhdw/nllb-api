from typing import (
    Awaitable,
    Callable,
    Literal,
    Mapping,
    TypedDict,
)

from starlette.applications import Starlette

class HttpStartMessage(TypedDict):
    """
    Summary
    -------
    a type for the http start message in the ASGI protocol

    Attributes
    ----------
    type (Literal['http.response.start']) : the type of the message
    status (int) : the response status code
    headers (list[tuple[bytes, bytes]]) : the request headers
    """

    type: Literal['http.response.start']
    status: int
    headers: list[tuple[bytes, bytes]]

class HttpBodyMessage(TypedDict):
    """
    Summary
    -------
    a type for the http body message in the ASGI protocol

    Attributes
    ----------
    type (Literal['http.response.body']) : the type of the message
    body (bytes) : the message body
    """

    type: Literal['http.response.body']
    body: bytes

class Scope(TypedDict):
    """
    Summary
    -------
    a type for the scope in the ASGI protocol

    Attributes
    ----------
    type (Literal['http', 'websocket', 'lifespan']) : the type of the scope
    asgi (Mapping[str, str]) : the ASGI protocol information
    http_version (str) : the HTTP version
    server (tuple[str, int]) : the server ip and port
    client (tuple[str, int]) : the client ip and port
    scheme (Literal['http', 'https']) : the HTTP scheme
    root_path (str) : the application root path
    headers (list[tuple[bytes, bytes]]) : the request headers
    method (Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH']) : the HTTP method
    path (str) : the path to the endpoint
    raw_path (bytes) : the path to the endpoint in bytes
    query_string (bytes) : the query string parameters
    app (Starlette) : the application object
    """

    type: Literal['http', 'websocket', 'lifespan']
    asgi: Mapping[str, str]
    http_version: str
    server: tuple[str, int]
    client: tuple[str, int] | None
    scheme: Literal['http', 'https']
    root_path: str
    headers: list[tuple[bytes, bytes]]
    method: Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    path: str
    raw_path: bytes
    query_string: bytes
    app: Starlette

type Message = HttpStartMessage | HttpBodyMessage
type Send = Callable[[Message], Awaitable[None]]
type Receive = Callable[[], Awaitable[Message]]
type ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]
