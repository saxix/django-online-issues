import datetime
import os
import re
from typing import TYPE_CHECKING

import pytest
import responses

from issues.backends.github_repo import Backend as GithubRepoBackend

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
        "OPTIONS": {
            "API_TOKEN": os.environ["GITHUB_API_TOKEN"],
            "PROJECT": os.environ["GITHUB_PROJECT"],
            "SCREENSHOT_REPO_PATH": "screenshots/",
            "SCREENSHOT_BRANCH": "develop",
        }
    }
    req = rf.get("/test/", HTTP_REFERER="/from/")
    req.user = admin_user
    return GithubRepoBackend(req)


@pytest.mark.online
@pytest.mark.github
def test_create(request, backend: GithubRepoBackend, screenshot: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if request.node.get_closest_marker("withoutresponses") is None:
        responses.add(
            responses.GET,
            "https://api.github.com:443/repos/user/project",
            json={
                "url": "https://api.github.com/repos/user/project",
            },
        )
        responses.add(
            responses.PUT,
            re.compile(r"https://api.github.com:443/repos/user/project/contents/screenshots/issue-.*"),
            json={"content": "", "commit": "123"},
        )
        responses.add(
            responses.GET,
            re.compile(r"https://api.github.com:443/repos/user/project/contents/screenshots/issue-.*"),
            json={},
        )
        responses.add(responses.POST, "https://api.github.com:443/repos/user/project/issues", json={})

    data: "IssueFormCleanedData" = {
        "title": f"Issue {timestamp} - screenshot: {bool(screenshot)}",
        "description": "login does no work properly",
        "screenshot": screenshot,
        "add_screenshot": bool(screenshot),
        "type": "bug",
    }
    backend.create_ticket(data)
