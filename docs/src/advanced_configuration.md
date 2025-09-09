# Advanced Configuration

## Issue Template

You can customize the issue description by overriding the `ISSUE_TEMPLATE` setting. The default template is:

```
- User: {user}
- UserAgent: {user_agent}
- Remote IP: {remote_ip}
- Url: {url}
- Version: {version}
---
{description}

{screenshot}
```
#### Example:

```python
# settings.py

my_template = """
- User: {user}
- UserAgent: {user_agent}
- Remote IP: {remote_ip}
- Url: {url}
- Extra: {extras['environment']}
---
- {description}

"""

ISSUES = {
    "BACKEND": "issues.backends.gitlab.Backend",
    "ISSUE_TEMPLATE": my_template,
    "OPTIONS": {
        "API_TOKEN": "your_gitlab_private_access_token",
        "PROJECT": "your_project_id_or_path",
    },
    "ANNOTATIONS": {
        "get_extra_info": "mayapp.issues_config.get_extra_info"
    }
}
```
```
## Annotations


Annotations are a powerful feature that allows you to customize the data that are injected into the cotext description of the issue.
You can use them to add extra information to the issue description, such as the user's browser, the page they were on, or the version of your application. You can also use them to customize the labels that are added to the issue.

The `ANNOTATIONS` setting allows you to override the functions used to get extra information for the issue. The default functions are:

- `get_client_ip`: `issues.utils.get_client_ip`
- `get_extra_info`: `issues.utils.get_extra_info`
- `get_labels`: `issues.utils.get_labels`
- `get_version`: `issues.utils.get_version`
- `get_user`: `issues.utils.get_user`
- `get_user_agent`: `issues.utils.get_user_agent`

You can provide your own functions to customize the information that is sent with the issue.

### `get_client_ip`

```python
def get_client_ip(request: HttpRequest) -> str:
```

This function returns the client's IP address. The default implementation checks the following headers in order: `HTTP_X_ORIGINAL_FORWARDED_FOR`, `HTTP_X_FORWARDED_FOR`, `HTTP_X_REAL_IP`, `REMOTE_ADDR`.

### `get_extra_info`

```python
def get_extra_info(request: HttpRequest, data: dict[str, Any]) -> dict[str, Any]:
```

This function returns a dictionary of extra information to be added to the issue. The default implementation returns an empty dictionary.

### `get_labels`

```python
def get_labels(request: HttpRequest, original: list[str]) -> list[str]:
```

This function returns a list of labels for the issue. The default implementation returns the `type` provided by the form.

### `get_user`

```python
def get_user(request: "AuthenticatedHttpRequest") -> str:
```

This function returns the user's email address if the user is authenticated, otherwise it returns "N/A".

### `get_user_agent`

```python
def get_user_agent(request: HttpRequest) -> str:
```

This function returns the user's user agent string.

### `get_version`

```python
def get_version(request: HttpRequest) -> str:
```

This function should return the application version. The default implementation returns "N/A".
