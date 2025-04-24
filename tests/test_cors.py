# ruff: noqa: S101


from httpx import Response
from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark

from server.app import app, extract_cors_values
from server.config import Config


def get_language(response: Response) -> str | None:
    return response.json().get('language')


def get_confidence(response: Response) -> float | None:
    return response.json().get('confidence')


async def detect_language(client: AsyncTestClient[Litestar], text: str) -> Response:
    return await client.get('/v4/language', params={'text': text})


@mark.anyio
async def test_cors() -> None:
    Config.stub_language_detector = True
    Config.stub_translator = True

    Config.access_control_allow_origin = 'http://localhost:3000, example.com'
    Config.access_control_allow_method_get = False
    Config.access_control_allow_method_post = False
    Config.access_control_allow_method_options = True
    Config.access_control_allow_method_delete = False
    Config.access_control_allow_method_put = True
    Config.access_control_allow_method_patch = True
    Config.access_control_allow_method_head = True
    Config.access_control_allow_method_trace = True
    Config.access_control_allow_credentials = True
    Config.access_control_allow_headers = 'X-Custom-Header,Upgrade-Insecure-Requests'
    Config.access_control_expose_headers = 'Content-Encoding,Kuma-Revision'
    Config.access_control_max_age = 3600

    allow_methods_dict = {
        'GET': Config.access_control_allow_method_get,
        'POST': Config.access_control_allow_method_post,
        'PUT': Config.access_control_allow_method_put,
        'DELETE': Config.access_control_allow_method_delete,
        'OPTIONS': Config.access_control_allow_method_options,
        'PATCH': Config.access_control_allow_method_patch,
        'HEAD': Config.access_control_allow_method_head,
        'TRACE': Config.access_control_allow_method_trace,
    }

    async with AsyncTestClient(app=app()) as client:
        origin = 'http://localhost:3000'
        response = await client.get('/v4/', headers={'Origin': origin})

        assert response.headers['Access-Control-Allow-Origin'] == origin
        assert response.headers['Access-Control-Allow-Credentials'] == 'true'
        assert response.headers['Access-Control-Allow-Headers'] == 'upgrade-insecure-requests, x-custom-header'
        assert response.headers['Access-Control-Expose-Headers'] == 'Content-Encoding, Kuma-Revision'
        assert set(extract_cors_values(response.headers['Access-Control-Allow-Methods'])) == {
            method for method, is_allowed in allow_methods_dict.items() if is_allowed
        }


@mark.anyio
async def test_cors_max_age() -> None:
    Config.stub_language_detector = True
    Config.stub_translator = True

    Config.access_control_allow_origin = '*'
    Config.access_control_max_age = 3600

    async with AsyncTestClient(app=app()) as client:
        response = await client.options('/v4/', headers={'Origin': 'http://localhost:3000'})
        assert response.headers['Access-Control-Max-Age'] == '3600'
