# pylint: disable=missing-function-docstring,redefined-outer-name

from fastapi.testclient import TestClient
from pytest import fixture

from server import Server


@fixture()
def client():
    return TestClient(next(Server.initialise()))


def test_generate(client: TestClient):
    response = client.post('/v1/translate', json={
        'text': 'Hello, world!',
        'source': 'eng_Latn',
        'target': 'spa_Latn'
    }).json()

    assert response['text'] == '¡Hola, mundo!'
