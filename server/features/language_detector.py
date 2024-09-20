from fasttext import load_model
from fasttext.FastText import _FastText as FastText

from server.config import Config
from server.helpers import huggingface_file_download
from server.types.languages import Languages


class LanguageDetector:
    """
    Summary
    -------
    a static class for the Language Detector

    Methods
    -------
    detect(text: str) -> Languages
        detect the language of the input text
    """

    __slots__ = ('model',)

    def __init__(self, model: FastText):
        self.model = model

    def detect(self, text: str) -> Languages:
        """
        Summary
        -------
        detect the language of the input text

        Parameters
        ----------
        text (str) : the input to detect the language of

        Returns
        -------
        language (Languages) : the detected language
        """
        labels, _ = self.model.predict(text, k=5)
        return labels[0][9:]  # type: ignore


def get_language_detector() -> LanguageDetector:
    """
    Summary
    -------
    get the language detector

    Returns
    -------
    language_detector (LanguageDetector) : the language detector
    """
    return LanguageDetector(load_model(huggingface_file_download(Config.language_detector_model_name, 'model.bin')))
