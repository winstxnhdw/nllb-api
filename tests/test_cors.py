# ruff: noqa: S101


from collections.abc import Callable

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark

from server.app import extract_cors_values
from server.config import Config


@mark.anyio
async def test_cors(client_factory: Callable[[Config], AsyncTestClient[Litestar]]) -> None:
    config = Config()
    config.access_control_allow_origin = 'http://localhost:3000, example.com'
    config.access_control_allow_method_get = False
    config.access_control_allow_method_post = False
    config.access_control_allow_method_options = True
    config.access_control_allow_method_delete = False
    config.access_control_allow_method_put = True
    config.access_control_allow_method_patch = True
    config.access_control_allow_method_head = True
    config.access_control_allow_method_trace = True
    config.access_control_allow_credentials = True
    config.access_control_allow_headers = 'X-Custom-Header,Upgrade-Insecure-Requests'
    config.access_control_expose_headers = 'Content-Encoding,Kuma-Revision'
    config.access_control_max_age = 3600

    allow_methods_dict = {
        'GET': config.access_control_allow_method_get,
        'POST': config.access_control_allow_method_post,
        'PUT': config.access_control_allow_method_put,
        'DELETE': config.access_control_allow_method_delete,
        'OPTIONS': config.access_control_allow_method_options,
        'PATCH': config.access_control_allow_method_patch,
        'HEAD': config.access_control_allow_method_head,
        'TRACE': config.access_control_allow_method_trace,
    }

    origin = 'http://localhost:3000'

    async with client_factory(config) as client:
        response = await client.get('/v4/', headers={'Origin': origin})

    assert response.headers['Access-Control-Allow-Origin'] == origin
    assert response.headers['Access-Control-Allow-Credentials'] == 'true'
    assert response.headers['Access-Control-Allow-Headers'] == 'upgrade-insecure-requests, x-custom-header'
    assert response.headers['Access-Control-Expose-Headers'] == 'Content-Encoding, Kuma-Revision'
    assert set(extract_cors_values(response.headers['Access-Control-Allow-Methods'])) == {
        method for method, is_allowed in allow_methods_dict.items() if is_allowed
    }


@mark.anyio
async def test_cors_max_age(client_factory: Callable[[Config], AsyncTestClient[Litestar]]) -> None:
    config = Config()
    config.access_control_allow_origin = '*'
    config.access_control_max_age = 3600

    async with client_factory(config) as client:
        response = await client.options('/v4/', headers={'Origin': 'http://localhost:3000'})

    assert response.headers['Access-Control-Max-Age'] == '3600'
