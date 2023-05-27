from fastapi.responses import HTMLResponse

from server.api.root import root


@root.get('/', response_class=HTMLResponse)
async def index():
    """
    Summary
    -------
    the `/` route
    """
    return HTMLResponse(content='<h1>nllb-api</h1>')
