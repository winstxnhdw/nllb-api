from fasttext import load_model
from fasttext.FastText import _FastText as FastText  # type: ignore

from server.config import Config
from server.features.types.languages import Languages
from server.helpers import huggingface_file_download


class LanguageDetector:
    """
    Summary
    -------
    a static class for the Language Detector

    Methods
    -------
    load() -> None
        load the model

    detect(text: str) -> Languages
        detect the language of the input text
    """

    model: FastText

    @classmethod
    def load(cls):
        """
        Summary
        -------
        download and load the model
        """
        model_path = huggingface_file_download(Config.language_detector_model_name, 'model.bin')
        cls.model: FastText = load_model(model_path)

    @classmethod
    def detect(cls, text: str) -> Languages:
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
        return cls.model.predict(text, k=5)[0][0][9:]  # type: ignore
