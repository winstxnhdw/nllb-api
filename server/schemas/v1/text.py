from typing import Annotated

from msgspec import Meta, Struct


class Text(Struct, kw_only=True):
    """
    Summary
    -------
    the NLLB token count schema

    Attributes
    ----------
    text (str)
        source text of a single language
    """

    text: Annotated[
        str,
        Meta(min_length=1, description='source text of a single language', examples=['Hello, world!']),
    ]
