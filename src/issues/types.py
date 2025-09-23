from typing import TypedDict


class IssueFormCleanedData(TypedDict):
    type: str
    title: str
    description: str
    add_screenshot: bool
    screenshot: str
