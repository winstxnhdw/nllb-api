from asyncio import sleep, wrap_future
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle

from ctranslate2 import Translator as CTranslator
from transformers.models.nllb.tokenization_nllb_fast import NllbTokenizerFast

from server.config import Config
from server.features.types import Languages, TranslatorOptions
from server.helpers import huggingface_download


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

    __slots__ = ('translator', 'tokeniser', 'lock')

    def __init__(self):
        model_path = huggingface_download(Config.translator_model_name)
        options: TranslatorOptions = {
            'model_path': model_path,
            'device': 'cuda' if Config.use_cuda else 'cpu',
            'compute_type': 'auto',
            'inter_threads': Config.worker_count,
        }

        try:
            self.translator = CTranslator(**options, flash_attention=True)

        except ValueError:
            self.translator = CTranslator(**options)

        self.tokeniser: NllbTokenizerFast = NllbTokenizerFast.from_pretrained(model_path, local_files_only=True)
        self.lock = False

    def __enter__(self):
        self.lock = True

    def __exit__(self, *_):
        self.lock = False

    def translate(self, text: str, source_language: Languages, target_language: Languages) -> str:
        """
        Summary
        -------
        translate the input from the source language to the target language without the Python GIL

        Parameters
        ----------
        input (str) : the input to translate
        source_language (Languages) : the source language
        target_language (Languages) : the target language

        Returns
        -------
        translated_text (str) : the translated text
        """
        self.tokeniser.src_lang = source_language

        results = self.translator.translate_batch(
            (self.tokeniser(text).tokens(),),
            ([target_language],),
            batch_type='tokens',
            beam_size=1,
        )

        return self.tokeniser.decode(self.tokeniser.convert_tokens_to_ids(results[0].hypotheses[0][1:]))


class TranslatorPool:
    """
    Summary
    -------
    a static class that encapsulates a pool of translators

    Methods
    -------
    load() -> None
        load the translator pool

    translate(text: str, source_language: Languages, target_language: Languages) -> str
        translate the input from the source language to the target language using a pool of translators
    """

    @classmethod
    def load(cls):
        """
        Summary
        -------
        load the translator pool
        """
        cls.thread_pool = ThreadPoolExecutor()
        cls.pool = cycle([Translator() for _ in range(Config.translator_pool_count)])

    @classmethod
    async def translate(cls, text: str, source_language: Languages, target_language: Languages) -> str:
        """
        Summary
        -------
        translate the input from the source language to the target language using a pool of translators

        Parameters
        ----------
        input (str) : the input to translate
        source_language (Languages) : the source language
        target_language (Languages) : the target language

        Returns
        -------
        translated_text (str) : the translated text
        """
        for translator in cls.pool:
            if translator.lock:
                await sleep(0)
                continue

            with translator:
                return await wrap_future(
                    cls.thread_pool.submit(translator.translate, text, source_language, target_language)
                )

        raise RuntimeError('Translator pool has been exhausted. This should never happen.')
