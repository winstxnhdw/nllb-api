from collections.abc import Iterator
from pathlib import Path

from litestar.testing.client.subprocess_client import run_app
from pytest import fixture

from nllb import AsyncTranslatorClient, TranslatorClient


@fixture(scope="session")
def app_url() -> Iterator[str]:
    with run_app(Path(__file__).parent.parent.parent, "server.app:app", retry_timeout=5) as base_url:
        yield base_url


@fixture
def client_with_auth(app_url: str) -> TranslatorClient:
    return TranslatorClient(
        base_url=app_url,
        auth_token="testtoken",  # noqa: S106
    )


@fixture
def async_client_with_auth(app_url: str) -> AsyncTranslatorClient:
    return AsyncTranslatorClient(
        base_url=app_url,
        auth_token="testtoken",  # noqa: S106
    )


@fixture(scope="session")
def client(app_url: str) -> TranslatorClient:
    return TranslatorClient(base_url=app_url)


@fixture(scope="session")
def async_client(app_url: str) -> AsyncTranslatorClient:
    return AsyncTranslatorClient(base_url=app_url)
