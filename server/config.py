from typing import Callable

from pydantic_settings import BaseSettings


def singleton[T](callable_object: Callable[[], T]) -> T:
    """
    Summary
    -------
    a decorator to transform a callable/class to a singleton

    Parameters
    ----------
    callable_object (Callable[[], T]) : the callable to transform

    Returns
    -------
    instance (T) : the singleton
    """
    return callable_object()


@singleton
class Config(BaseSettings):
    """
    Summary
    -------
    the general config class

    Attributes
    ----------
    server_port (int) : the port to run the server on
    server_root_path (str) : the root path for the server
    worker_count (int) : the number of workers to use
    translator_threads (int) : the number of threads for the translator
    use_cuda (bool) : whether to use CUDA for inference
    translator_model_name (str) : the name of the translator model
    language_detector_model_name (str) : the name of the language detector model
    """

    server_port: int = 49494
    server_root_path: str = '/api'
    worker_count: int = 1
    translator_threads: int = 1
    use_cuda: bool = False
    translator_model_name: str = 'winstxnhdw/nllb-200-distilled-1.3B-ct2-int8'
    language_detector_model_name: str = 'facebook/fasttext-language-identification'
