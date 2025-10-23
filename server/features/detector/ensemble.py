from fasttext_pybind import fasttext

from language import LanguageDetector
from server.features.detector.protocol import LanguageDetectorProtocol
from server.features.detector.stub import LanguageDetectorStub
from server.utils import huggingface_file_download


def get_language_detector(repository: str, *, stub: bool) -> LanguageDetectorProtocol:
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
    language_detector (LanguageDetectorProtocol)
        the language detector
    """
    if stub:
        return LanguageDetectorStub()

    fast_model = fasttext()
    fast_model.loadModel(huggingface_file_download(repository, "model.bin"))

    return LanguageDetector(fast_model)
