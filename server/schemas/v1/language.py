from pydantic import BaseModel, Field

from server.features.types import Languages


class Language(BaseModel):
    """
    Summary
    -------
    the NLLB language schema

    Attributes
    ----------
    language (Languages) : the detected language
    """

    language: Languages = Field(examples=['eng_Latn'])
