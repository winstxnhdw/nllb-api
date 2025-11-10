from typing import Annotated

from msgspec import Meta, Struct


class Tokens(Struct, kw_only=True, frozen=True, gc=False):
    """
    Summary
    -------
    the Tokens schema

    Attributes
    ----------
    length (int)
        the number of tokens in the input text
    """

    length: Annotated[
        int,
        Meta(description="the number of tokens in the input text", examples=[512]),
    ]
