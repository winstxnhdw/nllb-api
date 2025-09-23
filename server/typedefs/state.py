from litestar.datastructures import State

from server.config import Config
from server.features.detector import LanguageDetectorProtocol
from server.features.translator import TranslatorProtocol


class AppState(State):
    """
    Summary
    -------
    the Litestar application state that will be injected into the routers

    Attributes
    ----------
    config (Config)
        the application configuration

    language_detector (LanguageDetectorProtocol)
        the language detector

    translator (TranslatorProtocol)
        the translator
    """

    config: Config
    language_detector: LanguageDetectorProtocol
    translator: TranslatorProtocol
