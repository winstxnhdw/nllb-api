import torch
from intel_extension_for_pytorch import optimize
from transformers import (AutoModelForSeq2SeqLM, NllbTokenizer,
                          PreTrainedTokenizer, pipeline)


class Translator:
    """
    Summary
    -------
    a singleton class for the NLLB translator

    Attributes
    ----------
    model_name (str) : the name of the model
    tokeniser (PreTrainedTokenizer) : the tokeniser
    model (AutoModelForSeq2SeqLM) : the model

    Methods
    -------
    translate(input: str, source_language: str, target_language: str) -> str | None
        translate the input from the source language to the target language
    """
    model_name = 'facebook/nllb-200-distilled-600M'
    tokeniser: PreTrainedTokenizer = NllbTokenizer.from_pretrained(model_name)
    model = optimize(AutoModelForSeq2SeqLM.from_pretrained(model_name))
    optimised_model = torch.compile(model, backend='ipex')


    @classmethod
    def translate(cls, text: str, source_language: str, target_language: str) -> str | None:
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
        translated_text (str | None) : the translated text
        """
        translator = pipeline(
            'translation',
            cls.optimised_model,
            tokenizer=cls.tokeniser,
            src_lang=source_language,
            tgt_lang=target_language,
        )

        output = translator(text, max_length=1000)[0]  # type: ignore
        return output.get('translation_text')          # type: ignore
