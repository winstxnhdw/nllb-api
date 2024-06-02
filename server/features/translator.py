from ctranslate2 import Translator as CTranslator
from transformers.models.nllb.tokenization_nllb_fast import NllbTokenizerFast

from server.config import Config
from server.features.types import Languages, TranslatorOptions
from server.helpers import huggingface_download


class Translator:
    """
    Summary
    -------
    a static class for the NLLB translator

    Methods
    -------
    load() -> None
        load the model

    translate(input: str, source_language: str, target_language: str) -> str
        translate the input from the source language to the target language
    """

    tokeniser: NllbTokenizerFast
    translator: CTranslator

    @classmethod
    def load(cls):
        """
        Summary
        -------
        download and load the model
        """
        model_path = huggingface_download('winstxnhdw/nllb-200-distilled-1.3B-ct2-int8')
        options: TranslatorOptions = {
            'model_path': model_path,
            'device': 'cuda' if Config.use_cuda else 'cpu',
            'compute_type': 'auto',
            'inter_threads': Config.worker_count,
        }

        try:
            cls.translator = CTranslator(**options, flash_attention=True)

        except ValueError:
            cls.translator = CTranslator(**options)

        cls.tokeniser = NllbTokenizerFast.from_pretrained(model_path, local_files_only=True)

    @classmethod
    async def translate(cls, text: str, source_language: Languages, target_language: Languages) -> str:
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
        cls.tokeniser.src_lang = source_language

        result = next(
            cls.translator.translate_iterable(
                (cls.tokeniser(text).tokens(),),
                ([target_language],),
                batch_type='tokens',
                beam_size=1,
            )
        )

        return cls.tokeniser.decode(cls.tokeniser.convert_tokens_to_ids(result.hypotheses[0][1:]))
