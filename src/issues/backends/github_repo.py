import base64
import datetime

import github
from django.utils.text import slugify
from github import Github

from ..config import CONFIG
from ..forms import IssueFormCleanedData
from .github import Backend as GithubBackend


class Backend(GithubBackend):
    screenshot_supported = True

    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        screenshot_path = self.get_option("SCREENSHOT_REPO_PATH")
        screenshot_url = ""

        g = Github(auth=github.Auth.Token(self.get_option("API_TOKEN")))
        repo = g.get_repo(self.get_option("PROJECT"))

        if cleaned_data["screenshot"]:
            screenshot = cleaned_data["screenshot"].split(",")[1]
            screenshot_data = base64.b64decode(screenshot)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            slug = slugify(cleaned_data["title"])
            filename = f"{slug}_{timestamp}.png"
            path = f"{screenshot_path}{filename}"

            repo.create_file(
                path=path,
                message=f"Add screenshot for issue: {cleaned_data['title']}",
                content=screenshot_data,
                branch=self.get_option("SCREENSHOT_BRANCH"),
            )
            url = repo.get_contents(path).download_url  # type: ignore[union-attr]
            screenshot_url = f"![Screenshot]({url})"

        description = self.get_description({**cleaned_data, "screenshot_url": screenshot_url})

        repo.create_issue(
            title=cleaned_data["title"],
            body=description,
            labels=CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data["type"]]),
        )
        return True
