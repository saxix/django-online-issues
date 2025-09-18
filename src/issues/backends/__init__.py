from typing import TYPE_CHECKING

from ._base import BaseBackend

if TYPE_CHECKING:
    from django.http import HttpRequest


def get_backend(request: "HttpRequest") -> BaseBackend:
    from ..config import CONFIG

    backend_class: type[BaseBackend] = CONFIG.BACKEND
    return backend_class(request)


__all__ = ["get_backend", "BaseBackend"]
