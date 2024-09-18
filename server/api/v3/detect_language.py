from typing import Annotated

from litestar import get
from litestar.openapi.spec.example import Example
from litestar.params import Parameter

from server.schemas.v1 import Language
from server.state import AppState


@get('/detect_language', sync_to_thread=False, cache=True)
def detect_language(
    state: AppState,
    text: Annotated[
        str,
        Parameter(
            description='Sample text for language detection',
            max_length=20,
            min_length=1,
            examples=[
                Example(summary='English', description='Example text in English (eng_Latn)', value='Hello, world!'),
                Example(summary='Spanish', description='Example text in Spanish (spa_Latn)', value='¡Hola, mundo!'),
            ],
        ),
    ],
) -> Language:
    """
    Summary
    -------
    the `/detect_language` route detects the language of the input text
    """
    return Language(language=state.language_detector.detect(text))
