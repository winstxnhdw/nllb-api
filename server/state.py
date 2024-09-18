from litestar.datastructures import State

from server.features.language_detector import LanguageDetector
from server.features.translator import Translator


class AppState(State):
    """
    Summary
    -------
    the Litestar application state that will be injected into the routers

    Attributes
    ----------
    language_detector (LanguageDetector) : the language detector
    translator (Translator) : the translator
    """

    language_detector: LanguageDetector
    translator: Translator
