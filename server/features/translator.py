from typing import Any, Iterator
from unittest.mock import create_autospec

from ctranslate2 import Translator as CTranslator
from tokenizers import Encoding
from transformers.models.nllb.tokenization_nllb_fast import NllbTokenizerFast

from server.config import Config
from server.types import Languages
from server.utils import huggingface_download


class Translator:
    """
    Summary
    -------
    a class for the NLLB translator

    Methods
    -------
    translate_generator(text: str, source_language: Languages, target_language: Languages) -> Iterator[str]
        translate the input from the source language to the target language tokens using a pool of tokenisers

    translate(input: str, source_language: str, target_language: str) -> str
        translate the input from the source language to the target language using a pool of tokenisers

    translate_stream(input: str, source_language: str, target_language: str) -> Iterator[str]
        streams the translation input from the source language to the target language using a pool of tokenisers
    """

    __slots__ = ('translator', 'tokeniser')

    def __init__(self, translator: CTranslator, tokeniser: NllbTokenizerFast):
        tokeniser._switch_to_input_mode = lambda: None  # hack to keep NLLB tokeniser thread-safe

        self.tokeniser: NllbTokenizerFast = tokeniser
        self.translator = translator

    def translate_generator(self, text: str, source_language: Languages, target_language: Languages) -> Iterator[str]:
        """
        Summary
        -------
        translate the input from the source language to the target language tokens using a pool of tokenisers

        Parameters
        ----------
        input (str) : the input to translate
        source_language (Languages) : the source language
        target_language (Languages) : the target language

        Returns
        -------
        tokens (Iterator[str]) : the translated tokens
        """

        encoding: Encoding = self.tokeniser(text).encodings[0]  # type: ignore
        results = self.translator.generate_tokens([source_language] + encoding.tokens, (target_language,))
        next(results)  # skip the target language token

        return (result.token for result in results if not result.is_last)

    def translate(self, text: str, source_language: Languages, target_language: Languages) -> str:
        """
        Summary
        -------
        translate the input from the source language to the target language using a pool of tokenisers

        Parameters
        ----------
        input (str) : the input to translate
        source_language (Languages) : the source language
        target_language (Languages) : the target language

        Returns
        -------
        translated_text (str) : the translated text
        """
        return self.tokeniser.convert_tokens_to_string(
            list(self.translate_generator(text, source_language, target_language))
        )

    def translate_stream(self, text: str, source_language: Languages, target_language: Languages) -> Iterator[str]:
        """
        Summary
        -------
        streams the translation input from the source language to the target language using a pool of tokenisers

        Parameters
        ----------
        input (str) : the input to translate
        source_language (Languages) : the source language
        target_language (Languages) : the target language

        Returns
        -------
        translated_text (Iterator[str]) : the translated text
        """

        return (
            self.tokeniser.convert_tokens_to_string((token,))  # type: ignore
            for token in self.translate_generator(text, source_language, target_language)
        )


def get_translator() -> Translator:
    """
    Summary
    -------
    get the translator pool

    Returns
    -------
    translator (TranslatorPool) : the translator pool
    """
    if Config.stub_translator:
        return create_autospec(Translator)

    model_path = huggingface_download(Config.translator_model_name)
    tokeniser: Any = NllbTokenizerFast.from_pretrained(model_path, local_files_only=True)
    translator = CTranslator(
        model_path,
        'cuda' if Config.use_cuda else 'cpu',
        compute_type='auto',
        inter_threads=Config.translator_threads,
    )

    return Translator(translator, tokeniser)
