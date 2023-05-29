from pydantic import BaseModel


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
    text: str
    source: str
    target: str
