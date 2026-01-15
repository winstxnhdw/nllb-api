# ruff: noqa: S101

from nllb import LanguagePrediction, TranslatorClient


def get_language(response: LanguagePrediction) -> str:
    return response.language


def test_model_loading(client_with_auth: TranslatorClient) -> None:
    assert not client_with_auth.load_model()
    assert client_with_auth.unload_model()
    assert not client_with_auth.unload_model()
    assert client_with_auth.load_model()


def test_model_load_without_auth(client: TranslatorClient) -> None:
    assert not client.load_model()


def test_model_unload_without_auth(client: TranslatorClient) -> None:
    assert not client.unload_model()


def test_translate(client: TranslatorClient) -> None:
    assert client.translate("Hello, world!", source="eng_Latn", target="spa_Latn") == "¡Hola, mundo!"


def test_detect_language(client: TranslatorClient) -> None:
    assert get_language(client.detect_language("Hello, world! This is my house!")) == "eng_Latn"


def test_detect_language_with_confidence(client: TranslatorClient) -> None:
    prediction = client.detect_language(
        "Hello, world! This is my house!",
        fast_model_confidence_threshold=1.1,
        accurate_model_confidence_threshold=0.0,
    )

    assert get_language(prediction) == "eng_Latn"


def test_count_tokens(client: TranslatorClient) -> None:
    assert client.count_tokens("Hello, world!") == 7  # noqa: PLR2004
