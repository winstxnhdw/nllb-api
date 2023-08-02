# pylint: skip-file

from os import PathLike
from typing import Any, Self

from transformers.tokenization_utils_fast import PreTrainedTokenizerFast

class NllbTokenizerFast(PreTrainedTokenizerFast):

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str | PathLike[Any],
        *,
        src_lang: str | None = None,
        tgt_lang: str | None = None,
        **kwargs: Any
    ) -> Self: ...


    def set_src_lang_special_tokens(self, source_language: str) -> None: ...
