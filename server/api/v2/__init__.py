from litestar import Router

from server.api.v2.index import index
from server.api.v2.translate import TranslateController

v2 = Router('/v2', tags=['v2'], route_handlers=[index, TranslateController])
