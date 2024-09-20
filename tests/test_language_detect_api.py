# pylint: disable=missing-function-docstring,redefined-outer-name


from httpx import Response
from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark


def get_language(response: Response) -> str | None:
    return response.json().get('language')


def get_confidence(response: Response) -> float | None:
    return response.json().get('confidence')


async def detect_language(client: AsyncTestClient[Litestar], text: str) -> Response:
    return await client.get('/v3/detect_language', params={'text': text})


@mark.anyio
@mark.parametrize(
    'text, language',
    [
        ('She sells seashells.', 'eng_Latn'),
        ('Ella vende conchas.', 'spa_Latn'),
    ],
)
async def test_detect_language_api(client: AsyncTestClient[Litestar], text: str, language: str):
    response = await detect_language(client, text)

    assert get_language(response) == language
    assert isinstance(get_confidence(response), float)


@mark.anyio
async def test_detect_language_with_empty_text(client: AsyncTestClient[Litestar]):
    response = await detect_language(client, '')
    assert response.status_code == 400


@mark.anyio
async def test_detect_language_with_long_text(client: AsyncTestClient[Litestar]):
    text = (
        'She sells seashells by the seashore, '
        'The shells she sells are surely seashells. '
        'So if she sells shells on the seashore, '
        "I'm sure she sells seashore shells."
    )

    response = await detect_language(client, text)

    assert response.status_code == 400
