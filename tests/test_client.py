# ruff: noqa: S101

from nllb import LanguagePrediction, TranslatorClient


def get_language(response: LanguagePrediction) -> str:
    return response.language


def test_model_loading(subprocess_client_with_auth: TranslatorClient) -> None:
    assert not subprocess_client_with_auth.load_model()
    assert subprocess_client_with_auth.unload_model()
    assert not subprocess_client_with_auth.unload_model()
    assert subprocess_client_with_auth.load_model()


def test_model_load_without_auth(subprocess_client: TranslatorClient) -> None:
    assert not subprocess_client.load_model()


def test_model_unload_without_auth(subprocess_client: TranslatorClient) -> None:
    assert not subprocess_client.unload_model()


def test_translate(subprocess_client: TranslatorClient) -> None:
    assert subprocess_client.translate("Hello, world!", source="eng_Latn", target="spa_Latn") == "¡Hola, mundo!"


def test_detect_language(subprocess_client: TranslatorClient) -> None:
    assert get_language(subprocess_client.detect_language("Hello, world! This is my house!")) == "eng_Latn"


def test_detect_language_with_confidence(subprocess_client: TranslatorClient) -> None:
    prediction = subprocess_client.detect_language(
        "Hello, world! This is my house!",
        fast_model_confidence_threshold=1.1,
        accurate_model_confidence_threshold=0.0,
    )

    assert get_language(prediction) == "eng_Latn"


def test_count_tokens(subprocess_client: TranslatorClient) -> None:
    assert subprocess_client.count_tokens("Hello, world!") == 7  # noqa: PLR2004
