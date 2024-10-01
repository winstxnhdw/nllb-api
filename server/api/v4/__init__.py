from litestar import Router

from server.api.v4.index import index
from server.api.v4.language import language
from server.api.v4.languages import languages

v4 = Router('/v4', tags=['v4'], route_handlers=[index, language, languages])
