# pylint: skip-file

from typing import Literal

ComputeTypes = Literal[
    'default',
    'auto',
    'int8',
    'int8_float16',
    'int8_bfloat16',
    'int16',
    'float16',
    'bfloat16',
    'float32',
]


class TranslatorResults:
    hypotheses: list[list[str]]


class Translator:

    def __init__(
        self,
        model_path: str,
        device: Literal['cpu', 'cuda', 'auto'] = 'cpu',
        *,
        compute_type: ComputeTypes = 'default',
    ) -> None: ...


    def translate_batch(self, tokens: list[list[str]], *, target_prefix: list[list[str]]) -> list[TranslatorResults]: ...
