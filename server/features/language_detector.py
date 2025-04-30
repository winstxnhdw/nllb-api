from unittest.mock import create_autospec

from fasttext import load_model
from fasttext.FastText import _FastText as FastText

from server.typedefs import Score
from server.typedefs.language import Language
from server.utils import huggingface_file_download


class LanguageDetector:
    """
    Summary
    -------
    a static class for the Language Detector

    Methods
    -------
    detect(text: str) -> tuple[Language, Score]
        detect the language of the input text
    """

    __slots__ = ('model',)

    def __init__(self, model: FastText) -> None:
        self.model = model

    def detect(self, text: str) -> tuple[Language, Score]:
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
        language (Language)
            the detected language

        score (Score)
            the confidence score of the detected language
        """
        labels, scores = next(zip(*self.model.predict([text]), strict=True))

        return (
            labels[0][9:],  # pyright: ignore [reportReturnType]
            float(scores[0]),
        )


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

    return LanguageDetector(load_model(huggingface_file_download(repository, 'model.bin')))
