from os import environ as env
from typing import Type, TypeVar

T = TypeVar('T', bound=float | int | str)


def try_parse(value: str | T | None, expected_type: Type[T]) -> T | None:
    """
    Summary
    -------
    try to parse a value to a type

    Parameters
    ----------
    value (T) : the value to parse
    expected_type (type) : the expected type of the value

    Returns
    -------
    value (T | None) : the parsed value or None if the value is invalid
    """
    if value is None:
        return None

    try:
        return expected_type(value)

    except (TypeError, ValueError):
        return None


def get_config(
    key: str,
    expected_type: Type[T],
    exception: type[Exception],
    default: T | None = None
) -> T:
    """
    Summary
    -------
    get a config value from the environment

    Parameters
    ----------
    key (str) : the key to get the value from
    expected_type (Type[T]) : the expected type of the value
    exception (type[Exception]) : the exception to raise if the value is invalid
    default (T | None) : the default value to use if the value is not found

    Returns
    -------
    value (T) : the value of the environment variable
    """
    if (value := try_parse(env.get(key, default), expected_type)) is None:
        raise exception

    return value
