import sys
from typing import Any

from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: dict[str, Any]) -> bool:
        from ..config import CONFIG

        if "screenshot" in cleaned_data:
            cleaned_data["screenshot"] = "<screenshot>"
        else:
            cleaned_data["screenshot"] = "<screenshot not provided>"

        data = {
            "labels": CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data.get("type", "issue")]),
            **self.get_ticket_data(cleaned_data),
        }
        for k, v in data.items():
            sys.stdout.write(f"{k}: {v}")
        return True
