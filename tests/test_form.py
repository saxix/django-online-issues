import pytest

from issues.backends import BaseBackend
from issues.forms import IssueForm


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {"ANNOTATIONS": {"get_labels": lambda request, labels: labels}, "OPTIONS": {"MY_OPTION": 1}}
    req = rf.get("/test/")
    req.user = admin_user
    return BaseBackend(req)


def test_form(backend):
    form = IssueForm(
        data={
            "type": "bug",
            "title": "summary",
            "description": "description",
            "url": "url",
            "add_screenshot": False,
            "screenshot": None,
        },
        backend=backend,
    )
    assert form.is_valid()
