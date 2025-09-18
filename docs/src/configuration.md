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
    "RENDERER": "html2canvas-pro",
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

### Screenshot Renderer

The `RENDERER` option allows you to choose the JavaScript library used to capture screenshots of the web page when a user submits an issue. You can set this option within the `ISSUES` dictionary in your `settings.py`.

The available options are:

-   `"html2canvas"` (Default): Uses the [html2canvas](https://html2canvas.hertzen.com/) library. It is the default option and is generally reliable for most use cases.
-   `"dom-to-image"`: Uses the [dom-to-image](https://github.com/tsayen/dom-to-image) library. This can be a good alternative if you encounter issues with `html2canvas`.
-   `"html2canvas-pro"`: Uses the [html2canvas-pro](https://github.com/yorickshan/html2canvas-pro) library, which is a fork of `html2canvas` with additional features and improvements. It can be more accurate in rendering complex CSS and layouts.
-   `None`: Disables screenshot functionality. No screenshot will be taken or included in the issue.

**Example Configuration:**

```python
# settings.py

ISSUES = {
    # ... other settings
    "RENDERER": "html2canvas-pro",
}
```

If the `RENDERER` option is not specified, it defaults to `"html2canvas"`. If you wish to disable screenshots, you must explicitly set it to `None`.
