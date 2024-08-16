from functools import lru_cache
from typing import Callable

from pydantic_settings import BaseSettings


def cache[T](user_function: Callable[[type[T]], T]) -> Callable[[type[T]], T]:
    """
    Summary
    -------
    a specific decorator to cache the result of a function

    Parameters
    ----------
    user_function (Callable[[type[T]], T]) : the function to cache

    Returns
    -------
    wrapper (Callable[[type[T]], T]) : the wrapper function
    """
    return lru_cache(maxsize=None)(user_function)


@cache
def singleton[T](cls: type[T]) -> T:
    """
    Summary
    -------
    a decorator to make a class a singleton

    Parameters
    ----------
    cls (type[T]) : the class to make a singleton

    Returns
    -------
    instance (T) : the singleton instance
    """
    return cls()


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
    use_cuda (bool) : whether to use CUDA for inference
    translator_model_name (str) : the name of the translator model
    language_detector_model_name (str) : the name of the language detector model
    """

    server_port: int = 49494
    server_root_path: str = '/'
    worker_count: int = 1
    translator_pool_count: int = 2
    use_cuda: bool = False
    translator_model_name: str = 'winstxnhdw/nllb-200-distilled-1.3B-ct2-int8'
    language_detector_model_name: str = 'facebook/fasttext-language-identification'
