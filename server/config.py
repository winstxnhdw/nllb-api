from collections.abc import Callable

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
    """

    server_port: int = 49494
    server_root_path: str = '/api'
    worker_count: int = 1
    translator_threads: int = 1
    use_cuda: bool = False
    stub_language_detector: bool = False
    stub_translator: bool = False

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
