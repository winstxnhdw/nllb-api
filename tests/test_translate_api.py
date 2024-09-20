# pylint: disable=missing-function-docstring,redefined-outer-name


from typing import Awaitable, Callable

from httpx import Response
from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark

from server.types.languages import Languages


def get_translation(response: Response) -> str | None:
    return response.json().get('result')


async def translate_post(client: AsyncTestClient[Litestar], text: str, source: str, target: str) -> Response:
    return await client.post('/v3/translate', json={'text': text, 'source': source, 'target': target})


async def translate_get(client: AsyncTestClient[Litestar], text: str, source: str, target: str) -> Response:
    return await client.get('/v3/translate', params={'text': text, 'source': source, 'target': target})


@mark.anyio
@mark.parametrize('translate', [translate_post, translate_get])
@mark.parametrize(
    'text, source, target, translation',
    [
        ('Hello, world!', 'eng_Latn', 'spa_Latn', '¡Hola, mundo!'),
        ('我是一名软件工程师！', 'zho_Hans', 'spa_Latn', '¡Soy ingeniero de software!'),
    ],
)
async def test_translate_api(
    client: AsyncTestClient[Litestar],
    translate: Callable[[AsyncTestClient[Litestar], str, str, str], Awaitable[Response]],
    text: str,
    source: Languages,
    target: Languages,
    translation: str,
):
    response = await translate(client, text, source, target)
    assert get_translation(response) == translation


@mark.anyio
@mark.parametrize('translate', [translate_post, translate_get])
@mark.parametrize(
    'text, source, target',
    [('Hello, world!', '', 'spa_Latn'), ('Hello, world!', 'eng_Latn', ''), ('', 'eng_Latn', 'spa_Latn')],
)
async def test_translate_with_empty_fields(
    client: AsyncTestClient[Litestar],
    translate: Callable[[AsyncTestClient[Litestar], str, str, str], Awaitable[Response]],
    text: str,
    source: Languages,
    target: Languages,
):
    response = await translate(client, text, source, target)
    assert response.status_code == 400
