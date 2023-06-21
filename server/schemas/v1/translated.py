from pydantic import BaseModel, Field


class Translated(BaseModel):
    """
    Summary
    -------
    the translated schema

    Attributes
    ----------
    text (str) : the translated text
    """
    text: str = Field(example='¡Hola, mundo!')
