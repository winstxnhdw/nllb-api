from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from random import choice
from string import ascii_letters, digits

from aiohttp import ClientSession

from server.api import health
from server.lifespans.inject_state import inject_state
from server.typedefs import AppState


@inject_state
@asynccontextmanager
async def consul_register(_, state: AppState) -> AsyncIterator[None]:
    """
    Summary
    -------
    register the service with Consul

    Parameters
    ----------
    app (Litestar)
        the application instance
    """
    config = state.config

    if not config.consul_http_addr or not config.consul_service_address:
        yield
        return

    headers: dict[str, str] = {}
    consul_server = f'https://{config.consul_http_addr}/v1/agent/service'

    health_endpoint = (
        f'{config.consul_service_scheme}://{config.consul_service_address}:{config.consul_service_port}'
        f'{config.server_root_path}{health.paths.pop()}'
    )

    health_check = {
        'HTTP': health_endpoint,
        'Interval': '10s',
        'Timeout': '5s',
    }

    ascii_letters_with_digits = f'{ascii_letters}{digits}'
    payload = {
        'Name': config.app_name,
        'ID': f'{config.app_name}-{"".join(choice(ascii_letters_with_digits) for _ in range(4))}',  # noqa: S311
        'Tags': ['prometheus'],
        'Address': config.consul_service_address,
        'Port': config.consul_service_port,
        'Check': health_check,
        'Meta': {
            'metrics_port': f'{config.consul_service_port}',
            'metrics_path': '/metrics',
        },
    }

    if config.consul_auth_token:
        headers['Authorization'] = f'Bearer {config.consul_auth_token}'

    async with ClientSession(headers=headers) as session:
        async with session.put(
            f'{consul_server}/register',
            json=payload,
            params={'replace-existing-checks': 'true'},
        ) as response:
            response.raise_for_status()

        try:
            yield

        finally:
            async with session.put(f'{consul_server}/deregister/{payload["ID"]}'):
                pass
