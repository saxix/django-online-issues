from typing import TYPE_CHECKING, Any

from django.http import HttpRequest, HttpResponseRedirect

if TYPE_CHECKING:
    from issues.types import AuthenticatedHttpRequest


class HttpResponseRedirectToReferrer(HttpResponseRedirect):
    def __init__(self, request: HttpRequest, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        redirect_to = request.META.get("HTTP_REFERER", "/")
        super().__init__(redirect_to, False, *args, **kwargs)


def get_extra_info(request: HttpRequest, data: dict[str, Any]) -> dict[str, Any]:
    return {}


def get_client_ip(request: HttpRequest) -> str:
    for x in [
        "HTTP_X_ORIGINAL_FORWARDED_FOR",
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_REAL_IP",
        "REMOTE_ADDR",
    ]:
        ip = request.META.get(x)
        if ip:
            return str(ip.split(",")[0].strip())
    return ""


def get_labels(request: HttpRequest, original: list[str]) -> list[str]:
    return original


def get_user_agent(request: HttpRequest) -> str:
    ua_string = request.META.get("HTTP_USER_AGENT", "N/A")
    return str(ua_string)


def get_user(request: "AuthenticatedHttpRequest") -> str:
    if request.user.is_authenticated:
        return request.user.email  # type: ignore[no-any-return]
    return "N/A"


def get_version(request: HttpRequest) -> str:
    return "N/A"
