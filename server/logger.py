from __future__ import annotations

from logging import Logger as BaseLogger
from logging import getLogger


def redirect(logger_namespace: type[AppLogger]) -> BaseLogger:
    return logger_namespace.logger


@redirect
class AppLogger:
    logger = getLogger('custom.access')
