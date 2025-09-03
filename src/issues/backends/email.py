import base64
from typing import Any

import markdown
from django.core.mail import EmailMessage

from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: dict[str, Any]) -> bool:
        screenshot = cleaned_data.pop("screenshot")
        cleaned_data["screenshot"] = ""
        data = self.get_ticket_data(cleaned_data)
        html_output = markdown.markdown(data["description"])
        email = EmailMessage(
            subject=f"[{data['type']}] {data['title']}",
            body=data["description"],
            from_email=self.get_option("SENDER"),
            to=self.get_option("RECIPIENTS"),
        )
        email.attach("body", html_output, "text/html")
        if screenshot:
            base64_string = screenshot.split("base64,")[1]
            decoded_data = base64.b64decode(base64_string)
            email.attach("screenshot.png", decoded_data, "image/png")

        email.send()
        return True
