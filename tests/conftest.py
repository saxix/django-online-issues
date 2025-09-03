import base64
import os
import sys
from pathlib import Path

import pytest
import responses
from django_webtest import DjangoTestApp

here = Path(__file__).parent
sys.path.insert(0, str(here / "../src"))
sys.path.insert(0, str(here / "_extras"))


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        yield rsps


@pytest.fixture
def app(django_app_factory, admin_user) -> DjangoTestApp:
    django_app = django_app_factory(csrf_checks=False)
    django_app.set_user(admin_user)
    django_app._user = admin_user
    return django_app


@pytest.fixture
def image() -> str:
    file_path = Path(__file__).parent / "screenshot.png"
    with open(file_path, "rb") as f:
        image_data = f.read()
        encoded_string = base64.b64encode(image_data).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"


def pytest_configure(config):
    if not config.getoption("--online"):
        os.environ["GITLAB_API_TOKEN"] = "-not/available-"
        os.environ["GITHUB_API_TOKEN"] = "-not/available-"
        os.environ["GITLAB_PROJECT"] = "user/project"
        os.environ["GITHUB_PROJECT"] = "user/project"


def pytest_addoption(parser):
    parser.addoption("--online", action="store_true", default=False, help="add withoutresponses marker to online tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--online"):
        for item in items:
            if "online" in item.keywords:
                item.add_marker(pytest.mark.withoutresponses)

        # --online given in cli
        skip_gitlab = pytest.mark.skip(reason="GITLAB_API_TOKEN is not available")
        skip_github = pytest.mark.skip(reason="GITHUB_API_TOKEN is not available")

        gitlab_available = "GITLAB_API_TOKEN" in os.environ and "GITLAB_PROJECT" in os.environ
        github_available = "GITHUB_API_TOKEN" in os.environ and "GITHUB_PROJECT" in os.environ

        for item in items:
            if "gitlab" in item.keywords and not gitlab_available:
                item.add_marker(skip_gitlab)
            if "github" in item.keywords and not github_available:
                item.add_marker(skip_github)
