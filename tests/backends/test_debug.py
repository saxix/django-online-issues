from typing import TYPE_CHECKING

import pytest

from issues.backends.debug import Backend as DebugBackend

if TYPE_CHECKING:
    from issues.forms import IssueFormCleanedData


@pytest.fixture(params=[True, False])
def screenshot(request, image):
    if request.param:
        return image
    return ""


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {"ANNOTATIONS": {"get_labels": lambda request, labels: labels}}
    req = rf.get("/test/")
    req.user = admin_user
    return DebugBackend(req)


def test_create_ticket(backend: DebugBackend, screenshot):
    data: "IssueFormCleanedData" = {
        "title": "Test Issue",
        "url": "http://example.com",
        "type": "enhancement",
        "description": "This is a test description.",
        "add_screenshot": bool(screenshot),
        "screenshot": screenshot,
    }
    backend.create_ticket(data)

    assert backend.tickets
    assert backend.tickets[0]["title"] == "Test Issue"
    assert backend.tickets[0]["type"] == "enhancement"
    if bool(screenshot):
        assert backend.tickets[0]["screenshot_url"]
