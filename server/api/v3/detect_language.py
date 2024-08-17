from typing import Annotated

from litestar import get
from litestar.openapi.spec.example import Example
from litestar.params import Parameter

from server.features import LanguageDetector
from server.schemas.v1 import Language


@get('/detect_language', sync_to_thread=False, cache=True)
def detect_language(
    text: Annotated[str, Parameter(max_length=20, examples=[Example(value='Hello, world!')])],
) -> Language:
    """
    Summary
    -------
    the `/detect_language` route detects the language of the input text
    """
    return Language(language=LanguageDetector.detect(text))
