from typing import Annotated

from msgspec import Meta, Struct

from server.typedefs import Confidence, Language


class LanguageResult(Struct, kw_only=True, frozen=True, gc=False):
    """
    Summary
    -------
    the NLLB language schema

    Attributes
    ----------
    language (Languages)
        the detected language

    confidence (Score)
        the confidence score of the detected language
    """

    language: Annotated[Language, Meta(description="language code in the FLORES-200 format", examples=["eng_Latn"])]
    confidence: Annotated[Confidence, Meta(description="confidence score of the detected language")]
