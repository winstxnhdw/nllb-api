from typing import Protocol

from language import Prediction


class LanguageDetectorProtocol(Protocol):
    """
    Summary
    -------
    the language detector protocol

    Methods
    -------
    detect(text: str, *, fasttext_confidence_threshold: float, lingua_confidence_threshold: float) -> Prediction
        detect the language of the input text
    """

    def detect(
        self,
        text: str,
        *,
        fasttext_confidence_threshold: float,
        lingua_confidence_threshold: float,
    ) -> Prediction:
        """
        Summary
        -------
        detect the language of the input text

        Parameters
        ----------
        text (str)
            the input text to detect the language of

        fasttext_confidence_threshold (float)
            the confidence threshold for fasttext prediction

        lingua_confidence_threshold (float)
            the confidence threshold for lingua prediction

        Returns
        -------
        prediction (Prediction)
            the language prediction result
        """
        ...
