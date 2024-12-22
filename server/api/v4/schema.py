from typing import Any

from litestar import Request, get


@get('/schema', sync_to_thread=False)
def schema(request: Request[Any, Any, Any]) -> dict[str, Any]:
    """
    Summary
    -------
    the `/schema` route
    """
    return request.app.openapi_schema.to_schema()
