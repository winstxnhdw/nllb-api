from typing import Annotated

from msgspec import Meta, Struct

from server.typedefs import Languages


class Language(Struct, kw_only=True):
    """
    Summary
    -------
    the NLLB language schema

    Attributes
    ----------
    language (Languages)
        the detected language

    confidence (float)
        the confidence score of the detected language
    """

    language: Annotated[Languages, Meta(description='language code in the FLORES-200 format', examples=['eng_Latn'])]
    confidence: Annotated[float, Meta(description='confidence score of the detected language')]
