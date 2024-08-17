# pylint: disable=missing-function-docstring,redefined-outer-name


from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark


@mark.anyio
async def test_generate(client: AsyncTestClient[Litestar]):
    response = await client.post(
        '/v3/translate', json={'text': 'Hello, world!', 'source': 'eng_Latn', 'target': 'spa_Latn'}
    )

    assert response.json()['result'] == '¡Hola, mundo!'


@mark.anyio
async def test_generate_from_chinese(client: AsyncTestClient[Litestar]):
    response = await client.post(
        '/v3/translate', json={'text': '我是一名软件工程师！', 'source': 'zho_Hans', 'target': 'spa_Latn'}
    )

    assert response.json()['result'] == '¡Soy ingeniero de software!'
