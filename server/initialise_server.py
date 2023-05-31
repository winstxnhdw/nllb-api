from asyncio import run

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve

from server.api import v1
from server.config import Config


def initialise_server():
    """
    Summary
    -------
    initialize the server
    """
    app = FastAPI(docs_url='/')
    app.include_router(v1)
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

    run(serve(app, Config()))
