from typing import Generator

from ctranslate2 import Translator as CTranslator
from huggingface_hub import snapshot_download
from transformers.models.nllb.tokenization_nllb_fast import NllbTokenizerFast


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
    model_path = snapshot_download('winstxnhdw/nllb-200-distilled-1.3B-ct2-int8')
    tokeniser: NllbTokenizerFast = NllbTokenizerFast.from_pretrained(model_path)
    translator = CTranslator(model_path, compute_type='auto', inter_threads=8, intra_threads=1)

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
        cls.tokeniser.src_lang = source_language

        lines = [line for line in text.splitlines() if line]
        batches = map(cls.tokeniser, lines)
        tokens = map(lambda batch: batch.tokens(), batches)

        for result in cls.translator.translate_iterable(tokens, ([target_language] for _ in lines), beam_size=1):
            indices = cls.tokeniser.convert_tokens_to_ids(result.hypotheses[0][1:])
            yield f'{cls.tokeniser.decode(indices)}\n'
