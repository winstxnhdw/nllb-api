from typing import Annotated

from litestar import get
from litestar.exceptions import ClientException
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
            description='sample text for language detection',
            max_length=512,
            min_length=1,
            examples=[
                Example(summary='English', description='text in English (eng_Latn)', value='She sells seashells!'),
                Example(summary='Spanish', description='text in Spanish (spa_Latn)', value='Ella vende conchas!'),
            ],
        ),
    ],
    fast_model_confidence_threshold: Annotated[
        float,
        Parameter(
            query='fast-model-confidence-threshold',
            description='minimum acceptable confidence before using the accurate model results',
            ge=0.0,
            le=1.1,
            examples=[
                Example(summary='Default', description='hand-tuned threshold for general use', value=0.85),
                Example(summary='Max Accuracy', description='use the limited but accurate model', value=1.1),
                Example(summary='Max Throughput', description='use the fast but less accurate model', value=0.0),
            ],
        ),
    ] = 0.85,
    accurate_model_confidence_threshold: Annotated[
        float,
        Parameter(
            query='accurate-model-confidence-threshold',
            description='minimum acceptable confidence before falling back to the faster model results',
            ge=0.0,
            le=1.0,
            examples=[
                Example(summary='Default', description='hand-tuned threshold for general use', value=0.15),
                Example(summary='Max Accuracy', description='use the limited but accurate model', value=0.0),
            ],
        ),
    ] = 0.35,
) -> LanguageResult:
    """
    Summary
    -------
    the `/language` route detects the language of the input text
    """
    try:
        language, confidence = state.language_detector.detect(
            text,
            fast_model_confidence_threshold=fast_model_confidence_threshold,
            accurate_model_confidence_threshold=accurate_model_confidence_threshold,
        )

        return LanguageResult(language=language, confidence=confidence)

    except ValueError as error:
        raise ClientException(
            status_code=400,
            detail='Invalid input text. No newline character(s) are allowed!',
        ) from error
