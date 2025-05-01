from collections.abc import Sequence, Sized
from typing import Self

class Encoding(Sized):
    tokens: list[str]

class Tokenizer:
    @classmethod
    def from_file(cls, path: str) -> Self: ...
    def decode(self, ids: Sequence[int], skip_special_tokens: bool = True) -> str: ...
    def decode_batch(self, ids: Sequence[Sequence[int]], skip_special_tokens: bool = True) -> list[str]: ...
    def encode(
        self,
        sequence: Sequence[str],
        pair: Sequence[str] | None = None,
        is_pretokenized: bool = False,
        add_special_tokens: bool = True,
    ) -> Encoding: ...
    def encode_batch(
        self,
        input: Sequence[Sequence[str]],  # noqa: A002
        is_pretokenized: bool = False,
        add_special_tokens: bool = True,
    ) -> list[Encoding]: ...
    def encode_batch_fast(
        self,
        input: Sequence[Sequence[str]],  # noqa: A002
        is_pretokenized: bool = False,
        add_special_tokens: bool = True,
    ) -> list[Encoding]: ...
