import pytest

from issues.backends import get_backend
from issues.backends.email import Backend as EmailBackend


@pytest.fixture(params=[True, False])
def screenshot(request, image):
    if request.param:
        return image
    return ""


@pytest.fixture
def backend(rf, settings, admin_user) -> EmailBackend:
    settings.ISSUES = {
        "BACKEND": "issues.backends.email.Backend",
        "OPTIONS": {"SENDER": "aaa@example.com", "RECIPIENTS": ["one@example.com"]},
    }
    req = rf.get("/test/", HTTP_REFERER="http://example.com")
    req.user = admin_user
    return get_backend(req)


def test_create(backend: EmailBackend, mailoutbox, screenshot: str):
    data = {
        "title": "login issue",
        "url": "http://example.com",
        "description": "login does not work properly.",
        "screenshot": screenshot,
        "type": "bug",
    }
    backend.create_ticket(data)
    assert mailoutbox[0].subject == "[bug] login issue"
    assert (
        mailoutbox[0].body
        == r"""
- User: admin@example.com
- Url: http://example.com
- Version: N/A
- UserAgent: N/A
- Remote IP: 127.0.0.1

---
login does not work properly.


"""
    )
