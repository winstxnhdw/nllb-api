from typing import Annotated

from litestar import get
from litestar.openapi.spec.example import Example
from litestar.params import Parameter

from server.schemas.v1 import LanguageResult
from server.typedefs import AppState


@get('/language', sync_to_thread=False, cache=True)
def language(
    state: AppState,
    text: Annotated[
        str,
        Parameter(
            description='Sample text for language detection',
            max_length=512,
            min_length=1,
            examples=[
                Example(summary='English', description='text in English (eng_Latn)', value='She sells seashells!'),
                Example(summary='Spanish', description='text in Spanish (spa_Latn)', value='Ella vende conchas!'),
            ],
        ),
    ],
) -> LanguageResult:
    """
    Summary
    -------
    the `/language` route detects the language of the input text
    """
    language, score = state.language_detector.detect(text)
    return LanguageResult(language=language, confidence=score)
