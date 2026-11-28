from contextlib import AbstractAsyncContextManager
from types import TracebackType

from aiohttp import ClientSession, ClientTimeout
from litestar.config.app import AppConfig
from litestar.plugins import InitPlugin
from yarl import URL

from server.api import health


class ConsulPlugin(InitPlugin, AbstractAsyncContextManager[None]):
    """
    Summary
    -------
    a Litestar plugin that registers the service with Consul on startup and deregisters it on shutdown

    Parameters
    ----------
    app_name (str)
        the name of the application

    app_id (str)
        the ID of the application instance

    consul_http_addr (str)
        the address of the Consul HTTP API (e.g. localhost:8500)

    consul_service_address (str)
        the address of the service to register with Consul

    consul_service_port (int)
        the port of the service to register with Consul

    consul_service_scheme (str)
        the scheme of the service to register with Consul (e.g. http or https)

    server_root_path (str)
        the root path of the server

    consul_auth_token (str?)
        an optional auth token for populating the `Authorization` header
    """

    __slots__ = ("app_id", "payload", "session")

    def __init__(
        self,
        *,
        app_name: str,
        app_id: str,
        consul_http_addr: str,
        consul_service_address: str,
        consul_service_port: int,
        consul_service_scheme: str,
        server_root_path: str,
        consul_auth_token: str | None = None,
    ) -> None:
        consul_headers: dict[str, str] = {}
        health_headers: dict[str, tuple[str, ...]] = {}
        health_endpoint = URL.build(
            scheme=consul_service_scheme,
            host=consul_service_address,
            port=consul_service_port,
            path=f"{server_root_path}{health.paths.pop()}",
        )

        health_check = {
            "HTTP": str(health_endpoint),
            "Interval": "1m",
            "Timeout": "10s",
            "Header": health_headers,
        }

        if consul_auth_token:
            consul_headers["Authorization"] = f"Bearer {consul_auth_token}"
            health_headers["Authorization"] = (consul_headers["Authorization"],)

        self.app_id = app_id
        self.payload = {
            "Name": app_name,
            "ID": self.app_id,
            "Tags": ["prometheus"],
            "Address": consul_service_address,
            "Port": consul_service_port,
            "Check": health_check,
            "Meta": {
                "metrics_port": str(consul_service_port),
                "metrics_path": "/metrics",
            },
        }

        self.session = ClientSession(
            base_url=URL(consul_http_addr) / "v1/agent/service/",
            headers=consul_headers,
            raise_for_status=True,
            timeout=ClientTimeout(total=10),
        )

    async def __aenter__(self) -> None:
        await self.session.__aenter__()

        async with self.session.put("register", json=self.payload, params={"replace-existing-checks": "true"}):
            pass

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        async with self.session.put(URL("deregister") / self.app_id):
            pass

        await self.session.__aexit__(exc_type, exc_value, traceback)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.lifespan.append(self)
        return app_config
