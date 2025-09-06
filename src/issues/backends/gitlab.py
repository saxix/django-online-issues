import base64

import gitlab

from ..forms import IssueFormCleanedData
from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        from ..config import CONFIG

        screenshot = cleaned_data["screenshot"]

        gl = gitlab.Gitlab(private_token=self.get_option("API_TOKEN"))
        gl.auth()
        project = gl.projects.get(self.get_option("PROJECT"))
        screenshot_url = ""
        if screenshot:
            snap = project.upload(
                "screenshot.png",
                base64.b64decode(str(cleaned_data["screenshot"][21:])),
            )
            screenshot_url = snap.get("markdown")  # type: ignore[assignment]
        description = self.get_description({**cleaned_data, "screenshot_url": screenshot_url})
        project.issues.create(
            {
                "title": cleaned_data["title"],
                "description": description,
                "labels": CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data["type"]]),
            }
        )
        return True
