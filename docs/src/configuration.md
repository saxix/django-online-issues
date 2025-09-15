# Configuration

1. Add `issues` to your `INSTALLED_APPS` in your `settings.py` file:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "issues",
]
```

2. Include the `django-online-issues` URLs in your main `urls.py` file:

```python
# urls.py

from django.urls import path, include

urlpatterns = [
    # ...
    path("ticketing/", include("issues.urls", namespace="issues")),
]
```

    You can now access the ticket creation form at `/ticketing/issue/create/`.

3. Configure the backend in your `settings.py`. By default, tickets are printed to the console. To use a different
   backend, like GitLab, define the `ISSUES` configuration:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.gitlab.Backend",
    "OPTIONS": {
        "API_TOKEN": "your_gitlab_private_access_token",
        "PROJECT": "your_project_id_or_path",
    },
    "ANNOTATIONS": {
        "get_client_ip": "issues.utils.get_client_ip",
        "get_extra_info": "issues.utils.get_extra_info",
        "get_labels": "issues.utils.get_labels",
        "get_user": "issues.utils.get_user",
        "get_user_agent": "issues.utils.get_user_agent",
        "get_version": "issues.utils.get_version",
    }
}
```

**Important**: Avoid hardcoding sensitive information like API tokens directly in your `settings.py` file. Consider
using environment variables or a dedicated secrets management solution for production environments.
