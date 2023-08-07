# pylint: skip-file

from typing import Callable, Literal, overload

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


class GenerationStepResult:
    batch_id: int
    is_last: bool
    log_prob: float | None
    step: int
    token: str
    token_id: int


class TranslationResult:
    attention: list[list[str]]
    hypotheses: list[list[str]]
    scores: list[float]


class AsyncTranslationResult:

    def done(self) -> bool: ...

    def result(self) -> TranslationResult: ...


class Translator:

    def __init__(
        self,
        model_path: str,
        device: Literal['cpu', 'cuda', 'auto'] = 'cpu',
        *,
        device_index: str | dict[str, str] = 'default',
        compute_type: ComputeTypes = 'default',
        inter_threads: int = 1,
        intra_threads: int = 0,
        max_queued_batches: int = 0,
        files: object = None,
    ) -> None: ...


    @overload
    def translate_batch(
        self,
        source: list[list[str]],
        target_prefix: list[list[str] | None] | None = None,
        *,
        max_batch_size: int = 0,
        batch_type: str = 'examples',
        asynchronous: Literal[False] = False,
        beam_size: int = 2,
        patience: float = 1,
        num_hypotheses: int = 1,
        length_penalty: float = 1,
        coverage_penalty: float = 0,
        repetition_penalty: float = 1,
        no_repeat_ngram_size: int = 0,
        disable_unks: bool = False,
        supress_sequences: list[list[str]] | None = None,
        end_token: str | list[str] | list[int] | None = None,
        return_end_token: bool = False,
        prefix_bias_beta: float = 0,
        max_input_length: int = 1024,
        max_decoding_length: int = 256,
        min_decoding_length: int = 1,
        use_vmap: bool = False,
        return_scores: bool = False,
        return_attention: bool = False,
        return_alternatives: bool = False,
        min_alternative_expansion_prob: float = 0,
        sampling_topk: int = 1,
        sampling_topp: float = 1,
        sampling_temperature: float = 1,
        replace_unknowns: bool = False,
        callback: Callable[[GenerationStepResult], bool] | None = None
    ) -> list[TranslationResult]: ...


    @overload
    def translate_batch(
        self,
        source: list[list[str]],
        target_prefix: list[list[str] | None] | None = None,
        *,
        max_batch_size: int = 0,
        batch_type: str = 'examples',
        asynchronous: Literal[True],
        beam_size: int = 2,
        patience: float = 1,
        num_hypotheses: int = 1,
        length_penalty: float = 1,
        coverage_penalty: float = 0,
        repetition_penalty: float = 1,
        no_repeat_ngram_size: int = 0,
        disable_unks: bool = False,
        supress_sequences: list[list[str]] | None = None,
        end_token: str | list[str] | list[int] | None = None,
        return_end_token: bool = False,
        prefix_bias_beta: float = 0,
        max_input_length: int = 1024,
        max_decoding_length: int = 256,
        min_decoding_length: int = 1,
        use_vmap: bool = False,
        return_scores: bool = False,
        return_attention: bool = False,
        return_alternatives: bool = False,
        min_alternative_expansion_prob: float = 0,
        sampling_topk: int = 1,
        sampling_topp: float = 1,
        sampling_temperature: float = 1,
        replace_unknowns: bool = False,
        callback: Callable[[GenerationStepResult], bool] | None = None
    ) -> list[AsyncTranslationResult]: ...
