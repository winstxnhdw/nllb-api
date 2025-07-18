# ruff: noqa: S101


from collections.abc import Callable

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark

from server.app import extract_cors_values
from server.config import Config


@mark.anyio
@mark.parametrize('is_allowed', [True, False])
async def test_cors(
    client_factory: Callable[[Config], AsyncTestClient[Litestar]],
    *,
    is_allowed: bool,
) -> None:
    config = Config()
    config.access_control_allow_origin = 'http://localhost:3000, example.com'
    config.access_control_allow_method_get = is_allowed
    config.access_control_allow_method_post = is_allowed
    config.access_control_allow_method_options = is_allowed
    config.access_control_allow_method_delete = is_allowed
    config.access_control_allow_method_put = is_allowed
    config.access_control_allow_method_patch = is_allowed
    config.access_control_allow_method_head = is_allowed
    config.access_control_allow_method_trace = is_allowed
    config.access_control_allow_credentials = is_allowed
    config.access_control_allow_headers = 'X-Custom-Header,Upgrade-Insecure-Requests'
    config.access_control_expose_headers = 'Content-Encoding,Kuma-Revision'
    config.access_control_max_age = 3600

    methods = {
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',
        'PATCH',
        'HEAD',
        'TRACE',
    }

    origin = 'http://localhost:3000'

    async with client_factory(config) as client:
        response = await client.get('/v4/', headers={'Origin': origin})

    assert response.headers['Access-Control-Allow-Origin'] == origin
    assert response.headers['Access-Control-Allow-Headers'] == 'upgrade-insecure-requests, x-custom-header'
    assert response.headers['Access-Control-Expose-Headers'] == 'Content-Encoding, Kuma-Revision'
    assert response.headers.get('Access-Control-Allow-Credentials') == str(is_allowed).lower() if is_allowed else None
    assert set(extract_cors_values(response.headers['Access-Control-Allow-Methods'])) == (
        methods if is_allowed else {}
    )


@mark.anyio
async def test_cors_max_age(client_factory: Callable[[Config], AsyncTestClient[Litestar]]) -> None:
    config = Config()
    config.access_control_allow_origin = '*'
    config.access_control_max_age = 3600

    async with client_factory(config) as client:
        response = await client.options('/v4/', headers={'Origin': 'http://localhost:3000'})

    assert response.headers['Access-Control-Max-Age'] == '3600'
