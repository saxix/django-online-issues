from typing import TYPE_CHECKING

from ._base import BaseBackend

if TYPE_CHECKING:
    from ..types import AuthenticatedHttpRequest


def get_backend(request: "AuthenticatedHttpRequest") -> BaseBackend:
    from ..config import CONFIG

    backend_class: type[BaseBackend] = CONFIG.BACKEND
    return backend_class(request)


__all__ = ["get_backend"]
