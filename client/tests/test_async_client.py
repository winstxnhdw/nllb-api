# ruff: noqa: S101

from pytest import mark

from nllb import AsyncTranslatorClient


@mark.anyio
async def test_model_loading(async_client_with_auth: AsyncTranslatorClient) -> None:
    assert not await async_client_with_auth.load_model()
    assert await async_client_with_auth.unload_model()
    assert not await async_client_with_auth.unload_model()
    assert await async_client_with_auth.load_model()


@mark.anyio
async def test_model_load_without_auth(async_client: AsyncTranslatorClient) -> None:
    assert not await async_client.load_model()


@mark.anyio
async def test_model_unload_without_auth(async_client: AsyncTranslatorClient) -> None:
    assert not await async_client.unload_model()


@mark.anyio
async def test_translate(async_client: AsyncTranslatorClient) -> None:
    assert await async_client.translate("Hello, world!", source="eng_Latn", target="spa_Latn") == "¡Hola, mundo!"


@mark.anyio
async def test_detect_language(async_client: AsyncTranslatorClient) -> None:
    prediction = await async_client.detect_language("Hello, world! This is my house!")
    assert prediction.language == "eng_Latn"


@mark.anyio
async def test_detect_language_with_confidence(async_client: AsyncTranslatorClient) -> None:
    prediction = await async_client.detect_language(
        "Hello, world! This is my house!",
        fast_model_confidence_threshold=1.1,
        accurate_model_confidence_threshold=0.0,
    )

    assert prediction.language == "eng_Latn"


@mark.anyio
async def test_count_tokens(async_client: AsyncTranslatorClient) -> None:
    assert await async_client.count_tokens("Hello, world!") == 7  # noqa: PLR2004
