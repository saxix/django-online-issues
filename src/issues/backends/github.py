import github
from github import Github

from ..config import CONFIG
from ..forms import IssueFormCleanedData
from ._base import BaseBackend


class Backend(BaseBackend):
    screenshot_supported = False

    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        description = self.get_description({**cleaned_data, "screenshot_url": ""})

        g = Github(auth=github.Auth.Token(self.get_option("API_TOKEN")))
        repo = g.get_repo(self.get_option("PROJECT"))
        repo.create_issue(
            title=cleaned_data["title"],
            body=description,
            labels=CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data["type"]]),
        )
        return True
