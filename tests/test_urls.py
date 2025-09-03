from django.urls import reverse


def test_issue_edit(db, app):
    url = reverse("issues:create")
    res = app.get(url)
    assert res.status_code == 200
