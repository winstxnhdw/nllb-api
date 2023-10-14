# pylint: skip-file

from os import PathLike
from typing import Any, Self

from transformers.tokenization_utils_base import (
    EncodedInput,
    PreTokenizedInput,
    TextInput,
    TruncationStrategy,
)
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
from transformers.utils import PaddingStrategy, TensorType

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


    def convert_ids_to_tokens(self, ids: list[int], skip_special_tokens: bool = False) -> list[str]: ...


    def encode(
        self,
        text: str | PreTokenizedInput | EncodedInput,
        *,
        text_pair: TextInput | PreTokenizedInput | EncodedInput | None = None,
        add_special_tokens: bool = True,
        padding: bool | str | PaddingStrategy = False,
        truncation: bool | str | TruncationStrategy | None = None,
        max_length: int | None = None,
        stride: int = 0,
        return_tensors: str | TensorType | None = None,
        **kwargs: Any
    ) -> list[int]: ...
