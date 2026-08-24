from language import LanguageDetector
from server.features.detector.protocol import LanguageDetectorProtocol
from server.features.detector.stub import LanguageDetectorStub


def get_language_detector(*, stub: bool) -> LanguageDetectorProtocol:
    """
    Summary
    -------
    get the language detector

    Parameters
    ----------
    stub (bool)
        whether to return a stub object

    Returns
    -------
    language_detector (LanguageDetectorProtocol)
        the language detector
    """
    return LanguageDetectorStub() if stub else LanguageDetector()
