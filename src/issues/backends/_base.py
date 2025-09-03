from typing import TYPE_CHECKING, Any, TypedDict

from issues.exceptions import IssueError
from issues.utils import get_client_ip, get_user, get_user_agent, get_version

if TYPE_CHECKING:
    from issues.types import AuthenticatedHttpRequest


class IssueData(TypedDict):
    title: str
    type: str
    description: str
    screenshot: str


class BaseBackend:
    def __init__(self, request: "AuthenticatedHttpRequest") -> None:
        self.request = request

    def get_option(self, name: str) -> Any:
        from issues.config import CONFIG

        try:
            return CONFIG.OPTIONS[name]
        except KeyError as e:
            raise IssueError("Issues backend Improperly configured") from e

    def get_description(self, parameters: dict[str, Any]) -> str:
        from issues.config import CONFIG

        template: str = CONFIG.ISSUE_TEMPLATE
        return template.format(
            user=get_user(self.request),
            user_agent=get_user_agent(self.request),
            remote_ip=get_client_ip(self.request),
            version=get_version(self.request),
            **parameters,
        )

    def get_ticket_data(self, infos: dict[str, Any]) -> IssueData:
        return {
            "title": infos.get("title", ""),
            "type": infos.get("type", "issue"),
            "description": self.get_description(infos),
            "screenshot": "",
        }

    def create_ticket(self, cleaned_data: dict[str, Any]) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement create_ticket")
