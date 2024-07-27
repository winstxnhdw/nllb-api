from asyncio import get_running_loop

from server.features import TranslatorPool


async def load_nllb_model():
    """
    Summary
    -------
    download and load the NLLB model
    """
    await get_running_loop().run_in_executor(None, TranslatorPool.load)
