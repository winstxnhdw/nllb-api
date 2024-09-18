from typing import Annotated

from msgspec import Meta, Struct

from server.types import Languages


class Translation(Struct):
    """
    Summary
    -------
    the NLLB translation schema

    Attributes
    ----------
    text (str) : source text of a single language
    source (Languages) : source language in the FLORES-200 code format
    target (Languages) : target language in the FLORES-200 code format
    """

    text: Annotated[
        str, Meta(max_length=8192, description='source text of a single language', examples=['Hello, world!'])
    ]

    source: Annotated[
        Languages, Meta(description='source language in the FLORES-200 code format', examples=['eng_Latn'])
    ]

    target: Annotated[
        Languages, Meta(description='target language in the FLORES-200 code format', examples=['spa_Latn'])
    ]
