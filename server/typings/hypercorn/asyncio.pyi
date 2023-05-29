from fastapi import FastAPI
from hypercorn import Config


async def serve(app: FastAPI, config: Config) -> None: ...
