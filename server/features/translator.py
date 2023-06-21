from ctranslate2 import Translator as CTranslator
from huggingface_hub import snapshot_download
from transformers.models.nllb import NllbTokenizerFast


class Translator:
    """
    Summary
    -------
    a static class for the NLLB translator

    Attributes
    ----------
    model_name (str) : the name of the model
    translator_model_path (str) : the path to the model
    tokeniser (NllbTokenizerFast) : the tokeniser
    translator (Translator) : the ctranslate2 translator object

    Methods
    -------
    translate(input: str, source_language: str, target_language: str) -> str
        translate the input from the source language to the target language
    """
    model_name = 'winstxnhdw/nllb-200-distilled-1.3B-ct2-int8'
    translator_model_path = snapshot_download(model_name)
    tokeniser: NllbTokenizerFast = NllbTokenizerFast.from_pretrained(model_name)
    translator = CTranslator(translator_model_path)

    @classmethod
    def translate(cls, text: str, source_language: str, target_language: str) -> str:
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
        source = cls.tokeniser.convert_ids_to_tokens(cls.tokeniser.encode(text))
        results = cls.translator.translate_batch([source], target_prefix=[[target_language]])
        target: list[str] = results[0].hypotheses[0][1:]

        return cls.tokeniser.decode(cls.tokeniser.convert_tokens_to_ids(target))
