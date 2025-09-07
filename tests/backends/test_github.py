import os
from typing import TYPE_CHECKING

import pytest
import responses

from issues.backends.github import Backend as GithubBackend

if TYPE_CHECKING:
    from issues.forms import IssueFormCleanedData


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {
        "OPTIONS": {
            "API_TOKEN": os.environ["GITHUB_API_TOKEN"],
            "GITHUB_PROJECT": os.environ["GITHUB_PROJECT"],
        }
    }
    req = rf.get("/test/", HTTP_REFERER="/from/")
    req.user = admin_user
    return GithubBackend(req)


@pytest.mark.online
@pytest.mark.github
def test_create(request, backend: GithubBackend, image: str):
    if request.node.get_closest_marker("withoutresponses") is None:
        responses.add(
            responses.GET,
            "https://api.github.com:443/repos/user/project",
            json={
                "url": "https://api.github.com/repos/user/project",
            },
        )
        responses.add(responses.POST, "https://api.github.com:443/repos/user/project/issues", json={})
    data: "IssueFormCleanedData" = {
        "title": "login issue",
        "description": "login does no work properly",
        "screenshot": image,
        "add_screenshot": True,
        "type": "bug",
    }
    backend.create_ticket(data)
