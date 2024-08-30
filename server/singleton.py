from typing import Callable


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
