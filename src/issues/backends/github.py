from typing import Any

import github
from github import Github

from ..config import CONFIG
from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: dict[str, Any]) -> bool:
        g = Github(auth=github.Auth.Token(self.get_option("API_TOKEN")))
        repo = g.get_repo(self.get_option("GITHUB_PROJECT"))
        cleaned_data["extras"] = CONFIG.ANNOTATIONS["get_extra_info"](self.request, cleaned_data)
        cleaned_data["screenshot"] = ""
        data = self.get_ticket_data(cleaned_data)
        repo.create_issue(
            title=data["title"],
            body=data["description"],
            labels=CONFIG.ANNOTATIONS["get_labels"](self.request, [data.get("type", "issue")]),
        )
        return True
