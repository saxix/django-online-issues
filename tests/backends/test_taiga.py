import os
import typing

import pytest
import responses

from issues.backends.taiga import Backend as TaigaBackend

if typing.TYPE_CHECKING:
    from issues.forms import IssueFormCleanedData


_ISSUES = {
    "BACKEND": "issues.backends.taiga",
    "TYPES": dict([x.split(",") for x in os.environ.get("TAIGA_ISSUES", "Bug,13;CR,999").split(";")]),
    "OPTIONS": {
        "API_URL": os.environ.get("TAIGA_URL", "https://api.taiga.io"),
        "API_TOKEN": os.environ.get("TAIGA_API_TOKEN", "token"),
        "PROJECT_ID": int(os.environ.get("TAIGA_PROJECT_ID", "999")),
    },
}


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = _ISSUES
    req = rf.get("/test/", HTTP_REFERER="/from/")
    req.user = admin_user
    return TaigaBackend(req)


@pytest.mark.online
@pytest.mark.taiga
def test_create_ticket_with_screenshot(request, backend: TaigaBackend, image: str):
    _base_url = _ISSUES["OPTIONS"]['API_URL'] + "/issues"
    responses.add(
        responses.POST,
        _base_url,
        json={"id": 1, "subject": "login issue"},
        status=201,
    )
    responses.add(
        responses.POST,
        f"{_base_url}/attachments",
        json={},
        status=201,
    )

    data: "IssueFormCleanedData" = {
        "title": "test taiga integration",
        "description": "example: login does no work properly",
        "screenshot": image,
        "add_screenshot": True,
        "type": list(_ISSUES["TYPES"].items())[0][1],
    }
    assert backend.create_ticket(data) is True
