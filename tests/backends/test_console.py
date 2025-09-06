import sys
from io import StringIO

import pytest

from issues.backends.console import Backend as ConsoleBackend


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {"ANNOTATIONS": {"get_labels": lambda request, labels: labels}}
    req = rf.get("/test/")
    req.user = admin_user
    return ConsoleBackend(req)


@pytest.mark.parametrize("screenshot", ["fake-base64_encoded_image_data", ""])
def test_create_ticket(backend: ConsoleBackend, screenshot):
    data = {
        "title": "Test Issue",
        "type": "bug",
        "description": "This is a test description.",
        "labels": ["bug", "test"],
    }
    if screenshot:
        data["screenshot"] = screenshot
    # Redirect stdout to capture print output
    old_stdout = sys.stdout
    sys.stdout = new_stdout = StringIO()

    try:
        result = backend.create_ticket(data)
    finally:
        sys.stdout = old_stdout  # Restore stdout

    assert result is True

    captured_output = new_stdout.getvalue()
    assert "Test Issue" in captured_output
    assert "bug" in captured_output
    assert "This is a test description." in captured_output
