from unittest.mock import create_autospec

from fasttext_pybind import fasttext

from language import LanguageDetector
from server.utils import huggingface_file_download


def get_language_detector(repository: str, *, stub: bool) -> LanguageDetector:
    """
    Summary
    -------
    get the language detector

    Parameters
    ----------
    repository (str)
        the repository to download the model from

    stub (bool)
        whether to return a stub object

    Returns
    -------
    language_detector (LanguageDetector)
        the language detector
    """
    if stub:
        return create_autospec(LanguageDetector)

    fast_model = fasttext()
    fast_model.loadModel(huggingface_file_download(repository, 'model.bin'))

    return LanguageDetector(fast_model)
