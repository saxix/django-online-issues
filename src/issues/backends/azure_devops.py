import base64
import io
import json

import markdown
import requests
from django.utils.text import slugify
from requests.auth import HTTPBasicAuth

from ..forms import IssueFormCleanedData
from ._base import BaseBackend


class Backend(BaseBackend):
    screenshot_supported = True

    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        server_url = self.get_option("SERVER_URL", "https://dev.azure.com")
        project = self.get_option("PROJECT")  # encode spaces if any
        pat = self.get_option("TOKEN")

        work_item_type = cleaned_data["type"]

        url = f"{server_url}/{project}/_apis/wit/workitems/${work_item_type}?api-version=7.1-preview.3"

        headers = {"Content-Type": "application/json-patch+json"}
        screenshot_url: str = ""
        md_url = ""
        screenshot_data = cleaned_data.get("screenshot")
        if screenshot_data:
            slug = slugify(cleaned_data["title"])
            filename = f"{slug}.png"

            image_data = base64.b64decode(screenshot_data.split(",")[1])
            stream = io.BytesIO(image_data)
            attachment_url = (
                f"{server_url}/{project}/_apis/wit/attachments?fileName={filename}&api-version=7.1-preview.3"
            )
            response = requests.post(
                attachment_url,
                data=stream,
                auth=("", pat),
                headers={"Content-Type": "application/octet-stream"},
                timeout=10,
            )
            response.raise_for_status()
            screenshot_url = response.json()["url"]
            md_url = f"![aa]({response.json()['url']})"

        description = self.get_description({**cleaned_data, "screenshot_url": md_url})
        data_issue = [
            {"op": "add", "path": "/fields/System.Title", "from": None, "value": cleaned_data["title"]},
            {
                "op": "add",
                "path": "/fields/System.Description",
                "from": None,
                "value": markdown.markdown(description),
            },
        ]

        response = requests.post(
            url, headers=headers, auth=HTTPBasicAuth("", pat), data=json.dumps(data_issue), timeout=10
        )
        if response.status_code == 200:  # noqa: PLR2004
            issue = response.json()
            work_item_id = issue["id"]
            if screenshot_data and screenshot_url:
                url = f"https://dev.azure.com/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3"
                data_attachment = [
                    {
                        "op": "add",
                        "path": "/relations/-",
                        "value": {
                            "rel": "AttachedFile",
                            "url": screenshot_url,
                            "attributes": {"comment": "Adding screenshot as evidence"},
                        },
                    }
                ]
                response = requests.patch(
                    url, headers=headers, auth=HTTPBasicAuth("", pat), data=json.dumps(data_attachment), timeout=10
                )
                response.raise_for_status()
            return True
        return False
