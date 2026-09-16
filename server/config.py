from os import environ
from typing import Self
from uuid import uuid4

from msgspec import Struct, convert, field


class Config(Struct, frozen=True, rename="upper", gc=False):
    app_name: str = "nllb-api"
    server_port: int = 49494
    server_root_path: str = "/api"
    worker_count: int = 1
    auth_token: str = field(default_factory=lambda: str(uuid4()))

    translator_repository: str = "winstxnhdw/nllb-200-distilled-1.3B-ct2-int8"
    translator_threads: int = 1
    stub_translator: bool = False
    testing: bool = False
    use_cuda: bool = False

    stub_language_detector: bool = False

    access_control_allow_origin: str = "*"
    access_control_allow_method_get: bool = True
    access_control_allow_method_post: bool = True
    access_control_allow_method_options: bool = True
    access_control_allow_method_delete: bool = True
    access_control_allow_method_put: bool = True
    access_control_allow_method_patch: bool = True
    access_control_allow_method_head: bool = True
    access_control_allow_method_trace: bool = True
    access_control_allow_credentials: bool = True
    access_control_allow_headers: str = "*"
    access_control_expose_headers: str = "*"
    access_control_max_age: int = 600

    otel_exporter_otlp_endpoint: str | None = None

    consul_http_addr: str | None = None
    consul_auth_token: str | None = None
    consul_service_address: str | None = None
    consul_service_port: int = 443
    consul_service_scheme: str = "https"

    @classmethod
    def from_os(cls) -> Self:
        return convert(environ, type=cls, strict=False)
