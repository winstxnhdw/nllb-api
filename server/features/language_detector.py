from unittest.mock import create_autospec

from fasttext import load_model
from fasttext.FastText import _FastText as FastText

from server.config import Config
from server.typedefs.languages import Languages
from server.utils import huggingface_file_download

type Score = float


class LanguageDetector:
    """
    Summary
    -------
    a static class for the Language Detector

    Methods
    -------
    detect(text: str) -> tuple[Languages, Score]
        detect the language of the input text
    """

    __slots__ = ('model',)

    def __init__(self, model: FastText) -> None:
        self.model = model

    def detect(self, text: str) -> tuple[Languages, Score]:
        """
        Summary
        -------
        detect the language of the input text

        Parameters
        ----------
        text (str)
            the input to detect the language of

        Returns
        -------
        language (Languages)
            the detected language

        score (Score)
            the confidence score of the detected language
        """
        labels, scores = next(zip(*self.model.predict([text]), strict=True))

        return (
            labels[0][9:],  # pyright: ignore [reportReturnType]
            float(scores[0]),
        )


def get_language_detector() -> LanguageDetector:
    """
    Summary
    -------
    get the language detector

    Returns
    -------
    language_detector (LanguageDetector)
        the language detector
    """
    if Config.stub_language_detector:
        return create_autospec(LanguageDetector)

    return LanguageDetector(
        load_model(huggingface_file_download('facebook/fasttext-language-identification', 'model.bin'))
    )
