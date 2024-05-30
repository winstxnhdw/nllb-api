from server.api.v3 import v3
from server.features import Translator
from server.schemas.v1 import Translated, Translation


@v3.post('/translate')
async def translate(request: Translation) -> Translated:
    """
    Summary
    -------
    the `/translate` route translates an input from a source language to a target language
    """
    return Translated(result=await Translator.translate(request.text, request.source, request.target))
