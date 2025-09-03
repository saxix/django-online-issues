# Configuration

1.  Add `issues` to your `INSTALLED_APPS` in your `settings.py` file:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "issues",
]
```

2.  Include the `django-issues` URLs in your main `urls.py` file:

```python
# urls.py

from django.urls import path, include

urlpatterns = [
    # ...
    path("ticketing/", include("issues.urls", namespace="issues")),
]
```
    You can now access the ticket creation form at `/ticketing/issue/create/`.

3.  Configure the backend in your `settings.py`. By default, tickets are printed to the console. To use a different backend, like GitLab, define the `ISSUES` configuration:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.gitlab.Backend",
    "OPTIONS": {
        "API_TOKEN": "your_gitlab_private_access_token",
        "PROJECT": "your_project_id_or_path",
    },
}
```
