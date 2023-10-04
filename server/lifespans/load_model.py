from asyncio import get_running_loop

from server.features import Translator


async def load_model():
    """
    Summary
    -------
    download and load the model
    """
    await get_running_loop().run_in_executor(
        None,
        Translator.load
    )
