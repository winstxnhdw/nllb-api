from litestar import Router

from server.api.v3.detect_language import detect_language
from server.api.v3.index import index
from server.api.v3.translate import TranslateController

v3 = Router('/v3', tags=['v3'], route_handlers=[index, detect_language, TranslateController])
