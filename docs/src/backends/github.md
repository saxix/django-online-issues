# GitHub Backend

**Path**: `issues.backends.github.Backend`

The GitHub backend creates an issue in a specified GitHub repository.

!!! note

    This backend does not support screenshot uploads.

### Options:

-   **API_TOKEN**: Your GitHub personal access token with appropriate repository permissions.

-   **PROJECT**: The username or organization and project name repository.

### Example:

```python
# settings.py

ISSUES = {
    "BACKEND": "issues.backends.github.Backend",
    "OPTIONS": {
        "API_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "PROJECT": "user/repo",
    }
}
```
