from asyncio import get_running_loop

from server.features.detect_language import LanguageDetector


async def load_fasttext_model():
    """
    Summary
    -------
    download and load the FastText model
    """
    await get_running_loop().run_in_executor(None, LanguageDetector.load)
