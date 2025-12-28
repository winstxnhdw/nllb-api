from litestar.datastructures import State

from server.features.detector import LanguageDetectorProtocol
from server.features.translator import TranslatorProtocol


class AppState(State):
    """
    Summary
    -------
    the Litestar application state that will be injected into the routers

    Attributes
    ----------
    language_detector (LanguageDetectorProtocol)
        the language detector

    translator (TranslatorProtocol)
        the translator
    """

    language_detector: LanguageDetectorProtocol
    translator: TranslatorProtocol
