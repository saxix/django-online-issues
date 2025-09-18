from typing import TypedDict

import pytest
from django.urls import reverse
from testutils.selenium import Browser

from issues.backends.debug import Backend as DebugBackend

pytestmark = pytest.mark.selenium


class TestConfig(TypedDict):
    screenshot: bool
    backend: type[DebugBackend]


@pytest.fixture(
    params=[
        ("html2canvas", True),
        ("html2canvas", False),
        ("dom-to-image", True),
        ("dom-to-image", False),
        (None, None),
    ],
    ids=[
        "html2canvas-True",
        "html2canvas-False",
        "dom-to-image-True",
        "dom-to-image-False",
        "no-render",
    ],
)
def matrix(request) -> tuple[str | None, bool]:
    return request.param


@pytest.fixture
def config(settings, matrix: tuple[str | None, bool]) -> TestConfig:
    settings.ISSUES = {
        "BACKEND": "issues.backends.debug.Backend",
        "OPTIONS": {"SENDER": "aaa@example.com", "RECIPIENTS": ["one@example.com"]},
        "RENDERER": matrix[0],
    }

    return {"screenshot": matrix[1], "backend": DebugBackend}


def test_crawl(browser: Browser, config: TestConfig) -> None:
    debug_backend = config["backend"]
    add_screenshot = config["screenshot"]

    url = reverse("admin:index")
    browser.login()
    browser.open(url)
    browser.click("#issue-opener")
    browser.select_option_by_text("select#id_type", "enhancement")
    browser.type("#id_title", "Issue Title")
    browser.click("#django-issues-form button[type='submit']")
    required_field = browser.get_element("#id_description")
    message = browser.execute_script("return arguments[0].validationMessage;", required_field)
    assert message.startswith("Please fill ")
    browser.type("#id_description", "Description....")
    if add_screenshot is not None:
        checkbox = browser.get_element("#id_add_screenshot")
        if add_screenshot != checkbox.is_selected():
            checkbox.click()

    browser.click("#django-issues-form button[type='submit']")
    browser.assert_element_not_visible("#django-issues-modal-overlay")

    assert debug_backend.tickets
    assert debug_backend.tickets[0]["title"] == "Issue Title"
    assert debug_backend.tickets[0]["type"] == "enhancement"
    if add_screenshot:
        assert debug_backend.tickets[0]["screenshot"]
    else:
        assert debug_backend.tickets[0]["screenshot"] == ""


def test_crawl_novalidate(browser: Browser, config: TestConfig):
    url = reverse("admin:index")
    browser.login()
    browser.open(url)
    browser.click("#issue-opener")
    browser.wait_for_element("#django-issues-form")
    browser.execute_script("document.getElementById('django-issues-form').setAttribute('novalidate', ''); ")

    browser.select_option_by_text("select#id_type", "enhancement")
    browser.click("#django-issues-form button[type='submit']")
    browser.assert_element_visible("#django-issues-form-error-container")
    browser.find_non_empty_text("#django-issues-form-error-container .django-issues-message")

    browser.type("#id_description", "Description....")
