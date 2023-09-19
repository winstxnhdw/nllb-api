# pylint: disable=missing-function-docstring,redefined-outer-name

from fastapi.testclient import TestClient
from pytest import fixture

from server import initialise


@fixture()
def client():
    return TestClient(initialise())


def test_generate(client: TestClient):
    response = client.post('/v2/translate', json={
        'text': 'Hello, world!',
        'source': 'eng_Latn',
        'target': 'spa_Latn'
    })

    assert response.text == '¡Hola, mundo!\n'

def test_generate_stream(client: TestClient):
    english_texts = ['Hello, world!', 'Today is a good day.', 'Hopefully, it will stay that way.']
    spanish_texts = ['¡Hola, mundo!', 'Hoy es un buen día.', 'Con suerte, seguirá así.']

    responses = client.post('/v2/translate', json={
        'text': '\n'.join(english_texts),
        'source': 'eng_Latn',
        'target': 'spa_Latn'
    }).iter_lines()

    for response, translation in zip(responses, spanish_texts):
        assert response == translation
