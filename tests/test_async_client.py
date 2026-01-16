# ruff: noqa: S101

from nllb import AsyncTranslatorClient


async def test_model_loading(subprocess_async_client_with_auth: AsyncTranslatorClient) -> None:
    assert not await subprocess_async_client_with_auth.load_model()
    assert await subprocess_async_client_with_auth.unload_model()
    assert not await subprocess_async_client_with_auth.unload_model()
    assert await subprocess_async_client_with_auth.load_model()


async def test_model_load_without_auth(subprocess_async_client: AsyncTranslatorClient) -> None:
    assert not await subprocess_async_client.load_model()


async def test_model_unload_without_auth(subprocess_async_client: AsyncTranslatorClient) -> None:
    assert not await subprocess_async_client.unload_model()


async def test_translate(subprocess_async_client: AsyncTranslatorClient) -> None:
    translation = await subprocess_async_client.translate("Hello, world!", source="eng_Latn", target="spa_Latn")
    assert translation == "¡Hola, mundo!"


async def test_detect_language(subprocess_async_client: AsyncTranslatorClient) -> None:
    prediction = await subprocess_async_client.detect_language("Hello, world! This is my house!")
    assert prediction.language == "eng_Latn"


async def test_detect_language_with_confidence(subprocess_async_client: AsyncTranslatorClient) -> None:
    prediction = await subprocess_async_client.detect_language(
        "Hello, world! This is my house!",
        fast_model_confidence_threshold=1.1,
        accurate_model_confidence_threshold=0.0,
    )

    assert prediction.language == "eng_Latn"


async def test_count_tokens(subprocess_async_client: AsyncTranslatorClient) -> None:
    assert await subprocess_async_client.count_tokens("Hello, world!") == 7  # noqa: PLR2004
