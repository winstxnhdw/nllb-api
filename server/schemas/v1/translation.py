from pydantic import BaseModel, Field

from server.features.types import Languages


class Translation(BaseModel):
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

    text: str = Field(examples=['Hello, world!'])
    source: Languages = Field(examples=['eng_Latn'])
    target: Languages = Field(examples=['spa_Latn'])
