from typing import Any

from ._base import BaseBackend


class Backend(BaseBackend):
    tickets: list[dict[str, Any]] = []

    def create_ticket(self, cleaned_data: dict[str, Any]) -> bool:
        from ..config import CONFIG

        data = {
            "labels": CONFIG.ANNOTATIONS["get_labels"](self.request, [cleaned_data.get("type", "issue")]),
            **self.get_ticket_data(cleaned_data),
        }

        self.tickets.append(data)
        return True
