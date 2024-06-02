# pylint: disable=missing-function-docstring,redefined-outer-name

from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from server import initialise


@fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(initialise()) as client:
        yield client


def test_generate(client: TestClient):
    response = client.post('/v3/translate', json={'text': 'Hello, world!', 'source': 'eng_Latn', 'target': 'spa_Latn'})

    assert response.json()['result'] == '¡Hola, mundo!'


def test_generate_from_chinese(client: TestClient):
    response = client.post(
        '/v3/translate', json={'text': '我是一名软件工程师！', 'source': 'zho_Hans', 'target': 'spa_Latn'}
    )

    assert response.json()['result'] == '¡Soy ingeniero de software!'


def test_generate_stream(client: TestClient):
    english_texts = ['Hello, world!', 'Today is a good day.', 'Hopefully, it will stay that way.']
    spanish_texts = ['¡Hola, mundo!', 'Hoy es un buen día.', 'Con suerte, seguirá así.']

    responses = client.post(
        '/v2/translate', json={'text': '\n'.join(english_texts), 'source': 'eng_Latn', 'target': 'spa_Latn'}
    ).iter_lines()

    for response, translation in zip(responses, spanish_texts):
        assert response == translation
