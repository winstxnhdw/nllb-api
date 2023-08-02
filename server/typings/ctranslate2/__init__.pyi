# pylint: skip-file

from typing import Sequence

class TranslatorResults:
    hypotheses: list[list[str]]


class Translator:

    def __init__(self, model_path: str) -> None: ...


    def translate_batch(self, tokens: Sequence[Sequence[str]], *, target_prefix: Sequence[Sequence[str]]) -> Sequence[TranslatorResults]: ...
