# ruff: noqa: S101

from asyncio import TaskGroup
from collections.abc import Awaitable, Callable

from httpx import Response
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_304_NOT_MODIFIED, HTTP_400_BAD_REQUEST
from litestar.testing import AsyncTestClient
from pytest import mark

from server.typedefs.language import Language


async def translate_post(client: AsyncTestClient[Litestar], text: str, source: str, target: str) -> Response:
    return await client.post('/v4/translator', json={'text': text, 'source': source, 'target': target})


async def translate_get(client: AsyncTestClient[Litestar], text: str, source: str, target: str) -> Response:
    return await client.get('/v4/translator', params={'text': text, 'source': source, 'target': target})


async def translate_stream(client: AsyncTestClient[Litestar], text: str, source: str, target: str) -> Response:
    return await client.get('/v4/translator/stream', params={'text': text, 'source': source, 'target': target})


async def count_tokens(client: AsyncTestClient[Litestar], text: str) -> Response:
    return await client.get('/v4/translator/tokens', params={'text': text})


async def load_model(client: AsyncTestClient[Litestar], *, auth_token: str, keep_cache: bool) -> Response:
    return await client.put(
        '/v4/translator',
        params={'keep_cache': keep_cache},
        headers={'Authorization': auth_token},
    )


async def unload_model(client: AsyncTestClient[Litestar], *, auth_token: str, to_cpu: bool) -> Response:
    return await client.delete(
        '/v4/translator',
        params={'to_cpu': to_cpu},
        headers={'Authorization': auth_token},
    )


@mark.anyio
async def test_token_count(session_client: AsyncTestClient[Litestar]) -> None:
    response = await count_tokens(session_client, 'Hello, world!')
    assert response.status_code == HTTP_200_OK
    assert response.json() == {'length': 7}


@mark.anyio
async def test_model_loading(client: AsyncTestClient[Litestar], auth_token: str) -> None:
    response = await load_model(client, auth_token=auth_token, keep_cache=False)
    assert response.status_code == HTTP_304_NOT_MODIFIED
    response = await unload_model(client, auth_token=auth_token, to_cpu=False)
    assert response.status_code == HTTP_204_NO_CONTENT
    response = await unload_model(client, auth_token=auth_token, to_cpu=False)
    assert response.status_code == HTTP_304_NOT_MODIFIED
    response = await load_model(client, auth_token=auth_token, keep_cache=False)
    assert response.status_code == HTTP_204_NO_CONTENT


@mark.anyio
@mark.parametrize('translate', [translate_post, translate_get])
@mark.parametrize(
    ('text', 'source', 'target', 'translation'),
    [
        ('Hello, world!', 'eng_Latn', 'spa_Latn', '¡Hola, mundo!'),
        ('我是一名软件工程师！', 'zho_Hans', 'spa_Latn', '¡Soy un ingeniero de software!'),  # noqa: RUF001
    ],
)
async def test_translate_api(
    session_client: AsyncTestClient[Litestar],
    translate: Callable[[AsyncTestClient[Litestar], str, str, str], Awaitable[Response]],
    text: str,
    source: Language,
    target: Language,
    translation: str,
) -> None:
    response = await translate(session_client, text, source, target)
    assert response.json().get('result') == translation


@mark.anyio
async def test_translate_stream_api(session_client: AsyncTestClient[Litestar]) -> None:
    response = await translate_stream(session_client, 'Hello, world!', 'eng_Latn', 'spa_Latn')
    assert response.headers['Content-Type'] == 'text/event-stream; charset=utf-8'


@mark.anyio
@mark.parametrize('translate', [translate_post, translate_get, translate_stream])
@mark.parametrize(
    ('text', 'source', 'target'),
    [('Hello, world!', '', 'spa_Latn'), ('Hello, world!', 'eng_Latn', ''), ('', 'eng_Latn', 'spa_Latn')],
)
async def test_translate_with_empty_fields(
    session_client: AsyncTestClient[Litestar],
    translate: Callable[[AsyncTestClient[Litestar], str, str, str], Awaitable[Response]],
    text: str,
    source: Language,
    target: Language,
) -> None:
    response = await translate(session_client, text, source, target)
    assert response.status_code == HTTP_400_BAD_REQUEST


@mark.anyio
async def test_parallelism(session_client: AsyncTestClient[Litestar]) -> None:
    async with TaskGroup() as task_group:
        tasks = [
            task_group.create_task(translate_post(session_client, 'Hello, world!', 'eng_Latn', 'spa_Latn'))
            for _ in range(3)
        ]

    assert all(task.result().status_code == HTTP_200_OK for task in tasks)
