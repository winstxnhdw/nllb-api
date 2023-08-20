from pydantic import BaseModel, Field


class Translation(BaseModel):
    """
    Summary
    -------
    the NLLB translation schema

    Attributes
    ----------
    text (str) : the text to translate
    source (str) : the source language
    target (str) : the target language
    """
    text: str = Field(examples=['Hello, world!'])
    source: str = Field(examples=['eng_Latn'])
    target: str = Field(examples=['spa_Latn'])
