import base64
from typing import Any

import gitlab

from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: dict[str, Any]) -> bool:
        from ..config import CONFIG

        gl = gitlab.Gitlab(private_token=self.get_option("API_TOKEN"))
        gl.auth()
        project = gl.projects.get(self.get_option("PROJECT"))
        screenshot = ""
        if cleaned_data["screenshot"]:
            snap = project.upload(
                "screenshot.png",
                base64.b64decode(str(cleaned_data["screenshot"][21:])),
            )
            screenshot = snap.get("markdown")  # type: ignore[assignment]
        cleaned_data["screenshot"] = screenshot
        cleaned_data["extras"] = CONFIG.ANNOTATIONS["get_extra_info"](self.request, cleaned_data)
        data = self.get_ticket_data(cleaned_data)
        project.issues.create(
            {
                "title": data["title"],
                "description": data["description"],
                "labels": CONFIG.ANNOTATIONS["get_labels"](self.request, [data.get("type", "issue")]),
            }
        )
        return True
