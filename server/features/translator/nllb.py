from collections.abc import Iterator
from pathlib import Path
from typing import Self

from ctranslate2 import Translator as CTranslator
from tokenizers import Tokenizer

from server.features.translator.protocol import TranslatorProtocol
from server.features.translator.stub import TranslatorStub
from server.typedefs import Language
from server.utils import huggingface_download


class Translator(TranslatorProtocol):
    """
    Summary
    -------
    a class for the NLLB translator

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

    __slots__ = ("tokeniser", "translator", "use_cuda")

    def __init__(self, translator: CTranslator, tokeniser: Tokenizer, *, use_cuda: bool) -> None:
        self.tokeniser = tokeniser
        self.translator = translator
        self.use_cuda = use_cuda

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        del self.tokeniser
        del self.translator

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
        if not self.translator.model_is_loaded:
            return False

        self.translator.unload_model(to_cpu=self.use_cuda and to_cpu)
        return True

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
        if self.translator.model_is_loaded:
            return False

        self.translator.load_model(keep_cache=self.use_cuda and keep_cache)
        return True

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
        return len(self.tokeniser.encode(text)) + 1

    def translate_generator(self, text: str, source_language: Language, target_language: Language) -> Iterator[int]:
        """
        Summary
        -------
        translate the input from the source language to the target language tokens

        Parameters
        ----------
        text (str)
            the input to translate

        source_language (Languages)
            the source language

        target_language (Languages)
            the target languages

        Returns
        -------
        token_indices (Iterator[int]) : the translated tokens indices
        """
        target_prefix = (target_language,)
        results = self.translator.generate_tokens(
            (source_language, *self.tokeniser.encode(text).tokens),
            target_prefix,
            max_decoding_length=1024,
            sampling_temperature=0,
            no_repeat_ngram_size=3,
            suppress_sequences=(target_prefix,),
        )

        return (result.token_id for result in results if not result.is_last)

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
        return self.tokeniser.decode(tuple(self.translate_generator(text, source_language, target_language)))

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

        return (
            self.tokeniser.decode((token,))
            for token in self.translate_generator(text, source_language, target_language)
        )


def get_translator(
    repository: str,
    *,
    translator_threads: int,
    stub: bool,
    testing: bool,
    use_cuda: bool,
) -> TranslatorProtocol:
    """
    Summary
    -------
    get the translator object

    Parameters
    ----------
    repository (str)
        the repository to download the model from

    translator_threads (int)
        the number of threads to use for the translator

    stub (bool)
        whether to return a stub object

    testing (bool)
        whether the application is running in testing mode

    use_cuda (bool)
        whether to use CUDA for inference

    Returns
    -------
    translator (TranslatorProtocol)
        the translator
    """
    if stub:
        return TranslatorStub()

    model_path = huggingface_download(repository)
    tokeniser = Tokenizer.from_file(str(Path(model_path) / "tokenizer.json"))
    translator = CTranslator(
        model_path,
        "cuda" if use_cuda else "cpu",
        compute_type="default" if testing else "auto",
        inter_threads=translator_threads,
    )

    return Translator(translator, tokeniser, use_cuda=use_cuda)
