from asyncio import run
from importlib import import_module
from os import sep, walk
from os.path import join
from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve

from server.api import v1
from server.config import Config


class Server:
    """
    Summary
    -------
    the server class

    Attributes
    ----------

    """
    def __init__(self):

        self.app: FastAPI
        self.api_directory = join('server', 'api')


    def convert_delimiters(self, string: str, old: str, new: str) -> str:
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


    def initialise_routes(self):
        """
        Summary
        -------
        initialise all routes
        """
        module_file_names = [
            join(root, file)
            for root, _, files in walk(self.api_directory)
            for file in files
            if not file.startswith('__') and file.endswith('.py')
        ]

        for file_name in module_file_names:
            converted_file_name = self.convert_delimiters(file_name[:-3], sep, '.')
            module_name = import_module(converted_file_name).__name__
            print(f" * {self.convert_delimiters(module_name[len(self.api_directory):], '.', sep)} route found!")


    def initialise_server(self):
        """
        Summary
        -------
        initialize the server
        """
        self.app = FastAPI()
        self.app.include_router(v1)
        self.app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*'],
        )


    @classmethod
    def initialise(cls) -> Generator[FastAPI, None, None]:
        """
        Summary
        -------
        initialises everything
        """
        self = cls()
        self.initialise_routes()
        self.initialise_server()

        yield self.app
        run(serve(self.app, Config()))
