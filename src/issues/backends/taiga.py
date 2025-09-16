import base64
import io
from typing import TYPE_CHECKING

import requests

from ._base import BaseBackend

if TYPE_CHECKING:
    from ..forms import IssueFormCleanedData


class Backend(BaseBackend):
    screenshot_supported = True

    def get_issue_choices(self) -> list[tuple[str, str]]:
        from issues.config import CONFIG

        return list((x, y) for x, y in CONFIG.TYPES.items())

    def create_ticket(self, cleaned_data: "IssueFormCleanedData") -> bool:
        description = self.get_description({**cleaned_data, "screenshot_url": ""})

        api_url = self.get_option("API_URL", "https://api.taiga.io/api/v1")
        api_token = self.get_option("API_TOKEN")
        project = int(self.get_option("PROJECT_ID"))

        screenshot = cleaned_data["screenshot"]

        headers = {
            "Authorization": f"Application {api_token}",
            "Content-Type": "application/json",
        }
        data = {
            "project": project,
            "subject": cleaned_data["title"],
            "description": description,
            "type": cleaned_data["type"],
        }
        response = requests.post(f"{api_url}/issues", headers=headers, json=data, timeout=10)
        response.raise_for_status()
        issue_data = response.json()

        if screenshot:
            headers.pop("Content-Type")
            image_data = base64.b64decode(screenshot.split(",")[1])
            stream = io.BytesIO(image_data)
            files = {"attached_file": ("screenshot.png", stream, "image/png")}
            form_data = {"project": project, "object_id": issue_data["id"]}
            attachment_response = requests.post(
                f"{api_url}/issues/attachments", headers=headers, data=form_data, files=files, timeout=10
            )
            attachment_response.raise_for_status()

        return True
