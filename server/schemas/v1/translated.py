from pydantic import BaseModel, Field


class Translated(BaseModel):
    """
    Summary
    -------
    the translated schema

    Attributes
    ----------
    result (str) : the translated text
    """
    result: str = Field(examples=['¡Hola, mundo!'])
