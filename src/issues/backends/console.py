import sys

from ..forms import IssueFormCleanedData
from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        from ..config import CONFIG

        if "screenshot" in cleaned_data:
            screenshot_url = "<screenshot>"
        else:
            screenshot_url = "<screenshot not provided>"

        data = {
            "title": cleaned_data["title"],
            "type": cleaned_data["type"],
            "description": self.get_description({**cleaned_data, "screenshot_url": screenshot_url}),
        }

        data = {
            "labels": CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data.get("type", "issue")]),
            **data,
        }
        for k, v in data.items():
            sys.stdout.write(f"{k}: {v}")
        return True
