from itertools import cycle
from typing import Iterable, Iterator, Self

from ctranslate2 import Translator as CTranslator
from transformers.models.nllb.tokenization_nllb_fast import NllbTokenizerFast

from server.config import Config
from server.utils import huggingface_download
from server.types import Languages


class Tokeniser:
    """
    Summary
    -------
    context manager for the NLLB tokeniser

    Methods
    -------
    encode(text: str) -> list[str]
        encode the input text

    decode(tokens: str | list[str]) -> str
        decode the input tokens
    """

    __slots__ = ('tokeniser', 'lock')

    def __init__(self, model_path: str):
        self.tokeniser: NllbTokenizerFast = NllbTokenizerFast.from_pretrained(model_path, local_files_only=True)
        self.lock = False

    def __call__(self, source_language: Languages) -> Self:
        self.tokeniser.src_lang = source_language
        return self

    def __enter__(self):
        self.lock = True

    def __exit__(self, *_):
        self.lock = False

    def encode(self, text: str) -> list[str]:
        """
        Summary
        -------
        encode the input text

        Parameters
        ----------
        text (str) : the input text

        Returns
        -------
        tokens (list[str]) : the tokenised input text
        """
        return self.tokeniser(text).tokens()

    def decode(self, tokens: str | Iterable[str]) -> str:
        """
        Summary
        -------
        decode the input tokens

        Parameters
        ----------
        tokens (str | list[str]) : the input tokens

        Returns
        -------
        text (str) : the decoded text
        """
        return self.tokeniser.decode(
            self.tokeniser.convert_tokens_to_ids(tokens),  # type: ignore
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )


class Translator:
    """
    Summary
    -------
    a class for the NLLB translator

    Methods
    -------
    translate(input: str, source_language: str, target_language: str) -> str
        translate the input from the source language to the target language
    """

    __slots__ = ('translator', 'tokeniser_pool')

    def __init__(self, translator: CTranslator, tokeniser_pool: Iterator[Tokeniser]):
        self.tokeniser_pool = tokeniser_pool
        self.translator = translator

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

        for tokeniser in self.tokeniser_pool:
            if tokeniser.lock:
                continue

            with tokeniser(source_language):
                source_tokens = tokeniser.encode(text)

            results = self.translator.generate_tokens(source_tokens, (target_language,))
            next(results)

            return tokeniser.decode(result.token for result in results if not result.is_last)

        raise RuntimeError('Tokeniser pool has been exhausted. This should never happen.')


def get_translator() -> Translator:
    """
    Summary
    -------
    get the translator pool

    Returns
    -------
    translator (TranslatorPool) : the translator pool
    """
    model_path = huggingface_download(Config.translator_model_name)
    tokeniser_pool = cycle([Tokeniser(model_path) for _ in range(Config.translator_threads)])
    translator = CTranslator(
        model_path,
        'cuda' if Config.use_cuda else 'cpu',
        compute_type='auto',
        inter_threads=Config.translator_threads,
    )

    return Translator(translator, tokeniser_pool)
