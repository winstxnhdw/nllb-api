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
    text: str = Field(example='Hello, world!')
    source: str = Field(example='eng_Latn')
    target: str = Field(example='spa_Latn')
