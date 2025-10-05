# ruff: noqa: S101

from collections.abc import Callable

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient
from pytest import mark

from server.app import extract_cors_values
from server.config import Config


@mark.anyio
@mark.parametrize('is_allowed', [True, False])
async def test_cors(
    client_factory_without_lifespans: Callable[[Config], AsyncTestClient[Litestar]],
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

    origin = 'http://localhost:3000'

    async with client_factory_without_lifespans(config) as client:
        response = await client.get('/health', headers={'Origin': origin})

    methods = set() if not is_allowed else {'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH', 'HEAD', 'TRACE'}
    allow_credentials_header = response.headers.get('Access-Control-Allow-Credentials', 'false')
    allow_methods_header = response.headers.get('Access-Control-Allow-Methods', '')

    assert allow_credentials_header == str(is_allowed).lower()
    assert set(extract_cors_values(allow_methods_header)) == methods
    assert response.status_code == HTTP_200_OK
    assert response.headers['Access-Control-Allow-Origin'] == origin
    assert response.headers['Access-Control-Allow-Headers'] == 'upgrade-insecure-requests, x-custom-header'
    assert response.headers['Access-Control-Expose-Headers'] == 'Content-Encoding, Kuma-Revision'


@mark.anyio
async def test_cors_max_age(client_factory_without_lifespans: Callable[[Config], AsyncTestClient[Litestar]]) -> None:
    config = Config()
    config.access_control_allow_origin = '*'
    config.access_control_max_age = 3600

    async with client_factory_without_lifespans(config) as client:
        response = await client.options('/health', headers={'Origin': 'http://localhost:3000'})

    assert response.headers['Access-Control-Max-Age'] == '3600'
