import pytest
from django.test import override_settings

from issues.templatetags.issues import issues_tags


@override_settings(DEBUG=True, ISSUES={"RENDERER": "html2canvas"})
def test_issues_tags_debug_true():
    html = issues_tags()

    assert "issues.js" in html
    assert "issues.min.js" not in html
    assert "html2canvas.js" in html
    assert "html2canvas.min.js" not in html
    assert 'data-engine="html2canvas"' in html


@override_settings(DEBUG=False, ISSUES={"RENDERER": "dom-to-image"})
def test_issues_tags_debug_false():
    html = issues_tags()

    assert "issues.min.js" in html
    assert "dom-to-image.min.js" in html
    assert 'data-engine="dom-to-image"' in html


@override_settings(ISSUES={"RENDERER": "invalid_renderer"})
def test_issues_tags_invalid_renderer():
    with pytest.raises(ValueError, match="Invalid value .* for RENDERER"):
        issues_tags()


@override_settings(ISSUES={"RENDERER": None})
def test_issues_tags_renderer_none():
    html = issues_tags()
    assert "issues.min.js" in html
    assert "html2canvas.min.js" not in html
    assert 'data-engine=""' in html


@override_settings(DEBUG=False, ISSUES={"RENDERER": ("html2canvas", "http://example.com/html2canvas.min.js")})
def test_issues_tags_custom_url():
    html = issues_tags()

    assert "issues.min.js" in html
    assert "http://example.com/html2canvas.min.js" in html
    assert 'data-engine="html2canvas"' in html
