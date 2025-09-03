import pytest
from django.urls import reverse
from testutils.selenium import Browser

from issues.backends.debug import Backend as DebugBackend

pytestmark = pytest.mark.selenium


@pytest.fixture(params=["html2canvas", "dom-to-image"])
def renderer(request):
    return request.param


@pytest.fixture
def debug_backend(settings, renderer: str) -> type[DebugBackend]:
    settings.ISSUES = {
        "BACKEND": "issues.backends.debug.Backend",
        "OPTIONS": {"SENDER": "aaa@example.com", "RECIPIENTS": ["one@example.com"]},
        "RENDERER": renderer,
    }

    return DebugBackend


def test_crawl(browser: Browser, debug_backend: DebugBackend):
    url = reverse("admin:index")
    browser.login()
    browser.open(url)
    browser.click("#issue-opener")
    browser.select_option_by_text("select#id_type", "enhancement")
    browser.type("#id_title", "Issue Title")
    browser.click("#django-issues-form button[type='submit']")
    required_field = browser.get_element("#id_description")
    message = browser.execute_script("return arguments[0].validationMessage;", required_field)
    assert message == "Please fill in this field."

    browser.type("#id_description", "Description....")
    browser.click("#django-issues-form button[type='submit']")

    browser.assert_element_not_visible("#django-issues-modal-overlay")

    assert debug_backend.tickets
    assert debug_backend.tickets[0]["title"] == "Issue Title"
    assert debug_backend.tickets[0]["type"] == "enhancement"
