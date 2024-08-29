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

    result: Annotated[
        str,
        Meta(
            description='translated text in the language specified within the `target` request field',
            examples=['¡Hola, mundo!'],
        ),
    ]
