from typing import TYPE_CHECKING, Any

from ..forms import IssueFormCleanedData
from ._base import BaseBackend

if TYPE_CHECKING:
    from ..types import AuthenticatedHttpRequest


class Backend(BaseBackend):
    tickets: list[dict[str, Any]] = []

    def __init__(self, request: "AuthenticatedHttpRequest") -> None:
        super().__init__(request)
        Backend.tickets = []

    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        from ..config import CONFIG

        screenshot_url = ""
        if cleaned_data["screenshot"]:
            screenshot_url = "<url>"

        data = {
            "title": cleaned_data["title"],
            "type": cleaned_data["type"],
            "description": self.get_description({**cleaned_data, "screenshot_url": screenshot_url}),
            "labels": CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data.get("type", "issue")]),
            "screenshot_url": screenshot_url,
            "screenshot": cleaned_data["screenshot"],
        }

        self.tickets.append(data)
        return True
