from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from consul import Consul

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

    consul_service_check = {
        'http': f'{Config.consul_service_scheme}://{Config.consul_service_address}:{Config.consul_service_port}/health',
        'interval': '10s',
        'timeout': '5s',
    }

    consul.agent.service.register(
        name=Config.consul_service_name,
        address=Config.consul_service_address,
        port=Config.consul_service_port,
        check=consul_service_check,
        token=Config.consul_service_token,
    )

    try:
        yield

    finally:
        consul.agent.service.deregister(
            service_id=Config.consul_service_name,
            token=Config.consul_service_token,
        )
