import base64

import markdown
from django.core.mail import EmailMessage

from ..forms import IssueFormCleanedData
from ._base import BaseBackend


class Backend(BaseBackend):
    def create_ticket(self, cleaned_data: IssueFormCleanedData) -> bool:
        screenshot = cleaned_data["screenshot"]
        description = self.get_description({**cleaned_data, "screenshot_url": ""})
        html_output = markdown.markdown(description)
        email = EmailMessage(
            subject=f"[{cleaned_data['type']}] {cleaned_data['title']}",
            body=description,
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
