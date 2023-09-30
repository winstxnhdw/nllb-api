from os import environ as env
from typing import Type, TypeVar

T = TypeVar('T')


def get_config(
    key: str,
    expected_type: Type[T],
    exception: type[Exception],
    default: T = None
) -> T:
    """
    Summary
    -------
    get a config value from the environment

    Parameters
    ----------
    key (str) : the key to get the value from
    expected_type (type) : the expected type of the value
    exception (type[Exception]) : the exception to raise if the value is invalid
    default (Any) : the default value to use if the value is not found

    Returns
    -------
    value (T) : the value of the environment variable
    """
    if not isinstance(value := env.get(key, default), expected_type):
        raise exception

    return value
