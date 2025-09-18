import datetime
import os
from typing import TYPE_CHECKING

import pytest
import responses

from issues.backends.azure_devops import Backend as AzureDevopsBackend

if TYPE_CHECKING:
    from issues.forms import IssueFormCleanedData


@pytest.fixture(params=[True, False])
def screenshot(request, image):
    if request.param:
        return image
    return ""


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {
        "BACKEND": "issues.backends.azure_devops.Backend",
        "TYPES": ("issue",),
        "OPTIONS": {
            "SERVER_URL": os.environ.get("DEVOPS_SERVER_URL", "https://dev.azure.com"),
            "PROJECT": os.environ.get("DEVOPS_PROJECT", "user/project"),
            "TOKEN": os.environ.get("DEVOPS_TOKEN", "fake-pat"),
        },
    }
    req = rf.get("/test/", HTTP_REFERER="/from/")
    req.user = admin_user
    return AzureDevopsBackend(req)


@pytest.mark.azure_devops
@pytest.mark.online
def test_create(request, backend: AzureDevopsBackend, screenshot: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    project = backend.get_option("PROJECT")  # encode spaces if any

    if request.node.get_closest_marker("withoutresponses") is None:
        responses.add(
            responses.POST,
            f"https://dev.azure.com/{project}/_apis/wit/workitems/$issue?api-version=7.1-preview.3",
            json={"id": 123},
        )
        responses.add(
            responses.POST,
            f"https://dev.azure.com/{project}/_apis/wit/attachments?fileName=issue-{timestamp}.png&api-version=7.1-preview.3",
            json={"url": "https://store/image.png"},
        )
        responses.add(
            responses.PATCH,
            f"https://dev.azure.com/{project}/_apis/wit/workitems/123?api-version=7.1-preview.3",
            json={"url": "https://store/image.png"},
        )

    data: "IssueFormCleanedData" = {
        "title": f"Issue {timestamp}",
        "description": "login does no work properly",
        "screenshot": screenshot,
        "add_screenshot": bool(screenshot),
        "type": "issue",
    }
    assert backend.create_ticket(data)


@pytest.mark.azure_devops
@pytest.mark.online
def test_failure(request, backend: AzureDevopsBackend, screenshot: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    project = backend.get_option("PROJECT")  # encode spaces if any

    if request.node.get_closest_marker("withoutresponses") is None:
        responses.add(
            responses.POST,
            f"https://dev.azure.com/{project}/_apis/wit/workitems/$issue?api-version=7.1-preview.3",
            json={"id": 123},
            status=400,
        )
        responses.add(
            responses.POST,
            f"https://dev.azure.com/{project}/_apis/wit/attachments?fileName=issue-{timestamp}.png&api-version=7.1-preview.3",
            json={"url": "https://store/image.png"},
        )

    data: "IssueFormCleanedData" = {
        "title": f"Issue {timestamp}",
        "description": "login does no work properly",
        "screenshot": screenshot,
        "add_screenshot": bool(screenshot),
        "type": "issue",
    }
    assert not backend.create_ticket(data)
