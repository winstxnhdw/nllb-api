from collections.abc import Callable
from uuid import uuid4

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
    server_port (int)
        the port to run the server on

    server_root_path (str)
        the root path for the server

    worker_count (int)
        the number of workers to use

    translator_threads (int)
        the number of threads for the translator

    use_cuda (bool)
        whether to use CUDA for inference

    stub_language_detector (bool)
        whether to use a stub for the language detector

    stub_translator (bool)
        whether to use a stub for the translator

    language_detector_repository (str)
        the repository to download the language detector from

    translator_repository (str)
        the repository to download the translator from

    auth_token (str)
        the auth token to use for the server
    """

    server_port: int = 49494
    server_root_path: str = '/api'
    worker_count: int = 1
    auth_token: str = str(uuid4())

    translator_repository: str = 'winstxnhdw/nllb-200-distilled-1.3B-ct2-int8'
    translator_threads: int = 1
    stub_translator: bool = False
    use_cuda: bool = False

    language_detector_repository: str = 'facebook/fasttext-language-identification'
    stub_language_detector: bool = False

    access_control_allow_origin: str = '*'
    access_control_allow_method_get: bool = True
    access_control_allow_method_post: bool = True
    access_control_allow_method_options: bool = True
    access_control_allow_method_delete: bool = True
    access_control_allow_method_put: bool = True
    access_control_allow_method_patch: bool = True
    access_control_allow_method_head: bool = True
    access_control_allow_method_trace: bool = True
    access_control_allow_credentials: bool = True
    access_control_allow_headers: str = '*'
    access_control_expose_headers: str = '*'
    access_control_max_age: int = 600
