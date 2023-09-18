from typing import Generator

from ctranslate2 import Translator as CTranslator
from huggingface_hub import snapshot_download
from transformers.models.nllb import NllbTokenizerFast


class Translator:
    """
    Summary
    -------
    a static class for the NLLB translator

    Methods
    -------
    translate(input: str, source_language: str, target_language: str) -> str
        translate the input from the source language to the target language
    """
    model_name = 'winstxnhdw/nllb-200-distilled-1.3B-ct2-int8'
    translator_model_path = snapshot_download(model_name, max_workers=16)
    tokeniser: NllbTokenizerFast = NllbTokenizerFast.from_pretrained(model_name)
    translator = CTranslator(translator_model_path, compute_type='auto')

    @classmethod
    def translate(cls, text: str, source_language: str, target_language: str) -> Generator[str, None, None]:
        """
        Summary
        -------
        translate the input from the source language to the target language

        Parameters
        ----------
        input (str) : the input to translate
        source_language (str) : the source language
        target_language (str) : the target language

        Returns
        -------
        translated_text (str) : the translated text
        """
        cls.tokeniser.set_src_lang_special_tokens(source_language)

        lines = [line for line in text.splitlines() if line]
        indices = map(cls.tokeniser.encode, lines)
        tokens = map(cls.tokeniser.convert_ids_to_tokens, indices)

        for result in cls.translator.translate_iterable(tokens, ([target_language] for _ in lines)):
            yield cls.tokeniser.decode(
                cls.tokeniser.convert_tokens_to_ids(result.hypotheses[0][1:])
            )
