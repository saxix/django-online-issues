# Taiga Backend

**Path**: `issues.backends.taiga.Backend`

The Taiga backend creates an issue in a specified Taiga project.

### Types:

You will need to specify the dictionary mapping the ticket types with the relative IDs.

See [How to list issue types via API](https://docs.taiga.io/api.html#issue-types-list) or look at the admin console `/admin/projects/issuetype/`

### Options:

-   **API_URL**: [Optional] Your custom endpoint. Default = https://api.taiga.io/api/v1

-   **API_TOKEN**: Your Taiga private access token (see https://docs.taiga.io/api.html#auth-normal-login).

-   **PROJECT**: The numeric ID of your Taiga project (see the admin to get ID or use [API](https://docs.taiga.io/api.html#projects-get) ).

-   **TAGS**: The list of tags for the ticket

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.gitlab.Backend",
    "TYPES": {"Bug": 123, "Enhancement": 124},
    "OPTIONS": {
        "API_TOKEN": "xxxxxxxxxxxxxxxxxxxx",
        "PROJECT_ID": 123,
        "TAGS": [
            "online",
            "triage"
        ]
    }
}
```
