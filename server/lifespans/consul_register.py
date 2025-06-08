from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from consul import Consul

from server.api import health
from server.config import Config


@asynccontextmanager
async def consul_register(_) -> AsyncIterator[None]:
    """
    Summary
    -------
    register the service with Consul

    Parameters
    ----------
    app (Litestar)
        the application instance
    """
    if not Config.consul_service_address:
        yield
        return

    consul = Consul()

    if Config.consul_auth_token:
        consul.http.session.headers.update({'Authorization': Config.consul_auth_token})  # pyright: ignore [reportAttributeAccessIssue]

    health_endpoint = (
        f'{Config.consul_service_scheme}://{Config.consul_service_address}:{Config.consul_service_port}'
        f'{Config.server_root_path}{health.paths.pop()}'
    )

    consul_service_check = {
        'http': health_endpoint,
        'interval': '10s',
        'timeout': '5s',
    }

    consul.agent.service.register(
        name=Config.app_name,
        address=Config.consul_service_address,
        port=Config.consul_service_port,
        check=consul_service_check,
        token=Config.consul_service_token,
    )

    try:
        yield

    finally:
        consul.agent.service.deregister(
            service_id=Config.app_name,
            token=Config.consul_service_token,
        )
