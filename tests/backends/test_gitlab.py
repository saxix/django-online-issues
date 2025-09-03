import os

import pytest
import responses

from issues.backends.gitlab import Backend as GitlabBackend


@pytest.fixture(params=[True, False])
def screenshot(request, image):
    if request.param:
        return image
    return ""


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {
        "OPTIONS": {
            "API_TOKEN": os.environ["GITLAB_API_TOKEN"],
            "PROJECT": os.environ["GITLAB_PROJECT"],
        }
    }
    req = rf.get("/test/", HTTP_REFERER="/from/")
    req.user = admin_user
    return GitlabBackend(req)


@pytest.mark.online
def test_create(request, backend: GitlabBackend, screenshot: str):
    if request.node.get_closest_marker("withoutresponses") is None:
        responses.add(
            responses.GET,
            "https://gitlab.com/api/v4/user",
            json={
                "id": 2300979,
                "username": "user",
            },
        )
        responses.add(
            responses.GET,
            "https://gitlab.com/api/v4/projects/user%2Fproject",
            json={
                "id": 74143440,
                "_links": {
                    "issues": "https://gitlab.com/api/v4/projects/74143440/issues",
                },
            },
        )
        responses.add(responses.POST, "https://gitlab.com/api/v4/projects/74143440/uploads", json={})
        responses.add(responses.POST, "https://gitlab.com/api/v4/projects/74143440/issues", json={})
    data = {
        "title": "login issue",
        "url": "http://example.com",
        "description": "login does no work properly",
        "screenshot": screenshot,
        "labels": ["bug"],
    }
    backend.create_ticket(data)
