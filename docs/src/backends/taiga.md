# Taiga Backend

**Path**: `issues.backends.taiga.Backend`

The Taiga backend creates an issue in a specified Taiga project.

### Options:

-   **API_URL**: [Optional] Your custom endpoint. Default = https://api.taiga.io/api/v1

-   **API_TOKEN**: Your Taiga private access token (see https://docs.taiga.io/api.html#auth-normal-login).

-   **PROJECT**: The numeric ID of your Taiga project (see the admin to get ID or use [API](https://docs.taiga.io/api.html#projects-get) ).

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.gitlab.Backend",
    "OPTIONS": {
        "API_TOKEN": "xxxxxxxxxxxxxxxxxxxx",
        "PROJECT_ID": 123,
        "ISSUE_TYPE_ID": 321
    }
}
```
