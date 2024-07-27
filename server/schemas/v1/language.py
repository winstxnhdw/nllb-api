from typing import Annotated

from msgspec import Meta, Struct

from server.features.types import Languages


class Language(Struct):
    """
    Summary
    -------
    the NLLB language schema

    Attributes
    ----------
    language (Languages) : the detected language
    """

    language: Annotated[Languages, Meta(examples=['eng_Latn'])]
