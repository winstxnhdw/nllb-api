from collections.abc import Iterator
from typing import Self

from server.features.translator.protocol import TranslatorProtocol
from server.typedefs import Language


class TranslatorStub(TranslatorProtocol):
    """
    Summary
    -------
    a stub class for the translator

    Methods
    -------
    translate_generator(text: str, source_language: Language, target_language: Language) -> Iterator[str]
        translate the input from the source language to the target language tokens

    translate(text: str, source_language: Language, target_language: Language) -> str
        translate the input from the source language to the target language

    translate_stream(text: str, source_language: Language, target_language: Language) -> Iterator[str]
        streams the translation input from the source language to the target language

    unload_model(to_cpu: bool) -> bool
        unload the model from the current device

    load_model(keep_cache: bool) -> bool
        load the model back to the initial device

    count_tokens(text: str) -> int
        count the number of tokens in the input text
    """

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        pass

    def unload_model(self, *, to_cpu: bool) -> bool:
        """
        Summary
        -------
        unload the model from the current device

        Parameters
        ----------
        to_cpu (bool)
            whether to unload the model to CPU

        Returns
        -------
        success (bool)
            whether the model unload was executed
        """
        return to_cpu

    def load_model(self, *, keep_cache: bool) -> bool:
        """
        Summary
        -------
        load the model back to the initial device

        Parameters
        ----------
        keep_cache (bool)
            whether to keep the model cache in RAM

        Returns
        -------
        success (bool)
            whether the model load was executed
        """
        return keep_cache

    def count_tokens(self, text: str) -> int:
        """
        Summary
        -------
        count the number of tokens in the input text

        Parameters
        ----------
        text (str)
            the input text

        Returns
        -------
        token_count (int)
            the number of tokens that will be sent to the translator
        """
        return len(text.split())

    def translate(self, text: str, source_language: Language, target_language: Language) -> str:
        """
        Summary
        -------
        translate the input from the source language to the target language

        Parameters
        ----------
        text (str)
            the input to translate

        source_language (Languages)
            the source language

        target_language (Languages)
            the target language

        Returns
        -------
        translated_text (str)
            the translated text
        """
        return f"{text} from {source_language} to {target_language}"

    def translate_stream(self, text: str, source_language: Language, target_language: Language) -> Iterator[str]:
        """
        Summary
        -------
        streams the translation input from the source language to the target language

        Parameters
        ----------
        text (str)
            the input to translate

        source_language (Languages)
            the source language

        target_language (Languages)
            the target language

        Returns
        -------
        translated_text (Iterator[str])
            the translated text
        """
        yield from (f"{word} from {source_language} to {target_language}" for word in text.split())
