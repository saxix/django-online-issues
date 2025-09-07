from django.urls import reverse
from django_webtest import DjangoTestApp


def test_form_display(settings, app: DjangoTestApp):
    settings.ISSUES = {
        "BACKEND": "issues.backends.debug.Backend",
        "ISSUE_TEMPLATE": "{description}",
        "OPTIONS": {},
    }
    url = reverse("issues:create")
    res = app.get(url)
    assert res.status_code == 200, res.showbrowser()


def test_form_submit(settings, app: DjangoTestApp):
    settings.ISSUES = {
        "BACKEND": "issues.backends.debug.Backend",
        "ISSUE_TEMPLATE": "{description}",
        "OPTIONS": {},
    }
    url = reverse("issues:create")
    res = app.post_json(url, {}, expect_errors=True)
    assert res.status_code == 200
    assert res.json == {
        "errors": {
            "description": ["This field is required."],
            "title": ["This field is required."],
            "type": ["This field is required."],
        },
        "message": "Please correct the errors below.",
        "success": False,
    }


def test_form_error(settings, app: DjangoTestApp):
    settings.ISSUES = {
        "BACKEND": "issues.backends.debug.Backend",
        "ISSUE_TEMPLATE": "{description}",
        "OPTIONS": {},
    }
    url = reverse("issues:create")
    res = app.post(url, "", expect_errors=True)
    assert res.status_code == 400
    assert res.json == {
        "errors": "Invalid JSON payload.",
        "success": False,
    }
