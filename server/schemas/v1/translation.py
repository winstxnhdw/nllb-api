from typing import Annotated

from msgspec import Meta, Struct

from server.features.types import Languages


class Translation(Struct):
    """
    Summary
    -------
    the NLLB translation schema

    Attributes
    ----------
    text (str) : the text to translate
    source (Languages) : the source language
    target (Languages) : the target language
    """

    text: Annotated[str, Meta(examples=['Hello, world!'])]
    source: Annotated[Languages, Meta(examples=['eng_Latn'])]
    target: Annotated[Languages, Meta(examples=['spa_Latn'])]
