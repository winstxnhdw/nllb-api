# pylint: disable=missing-function-docstring,redefined-outer-name


from litestar import Litestar
from litestar.testing import AsyncTestClient


async def test_generate(client: AsyncTestClient[Litestar]):
    response = await client.post(
        '/v3/translate', json={'text': 'Hello, world!', 'source': 'eng_Latn', 'target': 'spa_Latn'}
    )

    assert response.json()['result'] == '¡Hola, mundo!'


async def test_generate_from_chinese(client: AsyncTestClient[Litestar]):
    response = await client.post(
        '/v3/translate', json={'text': '我是一名软件工程师！', 'source': 'zho_Hans', 'target': 'spa_Latn'}
    )

    assert response.json()['result'] == '¡Soy ingeniero de software!'


async def test_generate_stream(client: AsyncTestClient[Litestar]):
    english_texts = ['Hello, world!', 'Today is a good day.', 'Hopefully, it will stay that way.']
    spanish_texts = ['¡Hola, mundo!', 'Hoy es un buen día.', 'Con suerte, seguirá así.']

    responses = await client.post(
        '/v2/translate', json={'text': '\n'.join(english_texts), 'source': 'eng_Latn', 'target': 'spa_Latn'}
    )

    for response, translation in zip(responses.iter_lines(), spanish_texts):
        assert response == translation
