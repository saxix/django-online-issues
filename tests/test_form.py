from issues.forms import IssueForm


def test_form():
    form = IssueForm(
        data={
            "type": "bug",
            "title": "summary",
            "description": "description",
            "url": "url",
            "add_screenshot": False,
            "screenshot": None,
        }
    )
    assert form.is_valid()
