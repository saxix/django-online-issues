import pytest

from issues.backends._base import BaseBackend
from issues.exceptions import IssueError


@pytest.fixture
def backend(rf, settings, admin_user):
    settings.ISSUES = {"ANNOTATIONS": {"get_labels": lambda request, labels: labels}, "OPTIONS": {"MY_OPTION": 1}}
    req = rf.get("/test/")
    req.user = admin_user
    return BaseBackend(req)


def test_get_option(backend: BaseBackend):
    assert backend.get_option("MY_OPTION") == 1
    with pytest.raises(IssueError):
        assert backend.get_option("INVALID")
    assert backend.get_option("INVALID", "default") == "default"


def test_get_issue_types(backend: BaseBackend):
    assert backend.get_issue_choices()
