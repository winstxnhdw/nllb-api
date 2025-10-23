from types import SimpleNamespace

from language import Prediction
from server.features.detector.protocol import LanguageDetectorProtocol


class LanguageDetectorStub(LanguageDetectorProtocol):
    """
    Summary
    -------
    a stub class for the language detector

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
        language = (
            f"{text} with fasttext_confidence_threshold@{fasttext_confidence_threshold} and "
            f"lingua_confidence_threshold@{lingua_confidence_threshold}"
        )

        return SimpleNamespace({"language": language, "confidence": 1.0})  # pyright: ignore [reportReturnType]
