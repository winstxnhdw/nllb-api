from typing import TypeVar

from pydantic_settings import BaseSettings

T = TypeVar('T')


def singleton(cls: type[T]) -> T:
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
    port (int) : the port to run the server on
    server_root_path (str) : the root path for the server
    worker_count (int) : the number of workers to use
    document_index_prefix (str) : the prefix for the document index
    redis_index_name (str) : the name of the Redis index
    use_cuda (bool) : whether to use CUDA for inference
    """
    server_port: int = 49494
    server_root_path: str = '/api'
    worker_count: int = 1
    use_cuda: bool = False
