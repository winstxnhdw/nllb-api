from importlib import import_module
from itertools import chain
from os import walk


def convert_delimiters(string: str, old: str, new: str) -> str:
    """
    Summary
    -------
    convert delimiters in a string

    Parameters
    ----------
    string (str) : the string to convert
    old (str) : the old delimiter
    new (str) : the new delimiter

    Returns
    -------
    string (str) : the converted string
    """
    return new.join(string.split(old))


def initialise_routes():
    """
    Summary
    -------
    initialise all routes
    """
    api_directory = 'server/api'

    module_file_names = [
        [f'{root}/{file}' for file in files if not file.startswith('__') and file.endswith('.py')]
        for root, _, files in walk(api_directory)
    ]

    for file_name in chain.from_iterable(module_file_names):
        module_name = import_module(convert_delimiters(file_name[:-3], '/', '.')).__name__
        print(f" * {convert_delimiters(module_name[len(api_directory):], '.', '/')} route found!")
