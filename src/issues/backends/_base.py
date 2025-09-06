from typing import TYPE_CHECKING, Any, TypedDict

from issues.exceptions import IssueError
from issues.forms import IssueFormCleanedData

if TYPE_CHECKING:
    from issues.types import AuthenticatedHttpRequest


class IssueData(TypedDict):
    title: str
    type: str
    description: str


class BaseBackend:
    screenshot_supported: bool = True

    def __init__(self, request: "AuthenticatedHttpRequest") -> None:
        self.request = request

    def get_option(self, name: str) -> Any:
        from issues.config import CONFIG

        try:
            return CONFIG.OPTIONS[name]
        except KeyError as e:
            raise IssueError("Issues backend Improperly configured") from e

    def get_context(self) -> dict[str, Any]:
        from issues.config import CONFIG

        data = {
            "extras": {},
            "url": self.request.META.get("HTTP_REFERER", "N/A"),
            "user": CONFIG.ANNOTATIONS["get_user"](self.request),
            "user_agent": CONFIG.ANNOTATIONS["get_user_agent"](self.request),
            "version": CONFIG.ANNOTATIONS["get_version"](self.request),
            "remote_ip": CONFIG.ANNOTATIONS["get_client_ip"](self.request),
        }
        data["extras"] = CONFIG.ANNOTATIONS["get_extra_info"](self.request, data)
        return data

    def get_description(self, parameters: dict[str, Any]) -> str:
        from issues.config import CONFIG

        template: str = CONFIG.ISSUE_TEMPLATE
        return template.format(**self.get_context(), **parameters)

    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement create_ticket")
