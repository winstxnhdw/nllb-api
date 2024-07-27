from typing import Annotated

from msgspec import Meta, Struct


class Translated(Struct):
    """
    Summary
    -------
    the translated schema

    Attributes
    ----------
    result (str) : the translated text
    """

    result: Annotated[str, Meta(examples=['¡Hola, mundo!'])]
